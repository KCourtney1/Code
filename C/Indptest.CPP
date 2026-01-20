#include <iostream>
#include <vector>
#include <cmath>
#include <Eigen/Sparse>

class Exact {
public:
    Exact(double dx, double BC, double IC, double gamma, double epsilon) 
        : gamma(gamma), dx(dx), BC(BC), IC(IC), epsilon(epsilon) {
        update_dx(dx);
    }

    std::string toString() const {
        return "Exact";
    }

    double get_dx() const {
        return _dx;
    }

    void set_dx(double dx) {
        update_dx(dx);
    }

    void update_p() {
        for (int n = 0; n < N; ++n) {  // time loop
            for (int j = 0; j < M; ++j) {  // space loop
                double t = n * dt;
                double x = j * dx;

                if (((0 <= x && x <= 0.5) && (x > t)) || 
                    ((0.5 <= x && x <= 1) && (t <= (1 / (1 + epsilon) * (x - 0.5) + 0.5)))) {
                    p[n][j] = IC;
                } else {
                    p[n][j] = BC;
                }
            }
        }
    }

protected:
    double gamma;
    double dx;
    double BC;
    double IC;
    double epsilon;
    double dt;
    int M;
    int N;
    std::vector<std::vector<double>> p;

private:
    double _dx;

    void update_dx(double dx) {
        _dx = dx;
        dt = dx; 
        M = static_cast<int>(1 / dx);
        N = static_cast<int>(1 / dt);
        p.resize(N, std::vector<double>(M, 0));
    }
};

class Implicit : public Exact {
public:
    Implicit(double dx, double BC, double IC, double gamma, double epsilon) 
        : Exact(dx, BC, IC, gamma, epsilon) {}

    std::string toString() const {
        return "Implicit";
    }

    Eigen::SparseMatrix<double> get_coefficient_m_standard() {
        Eigen::VectorXd v = Eigen::VectorXd::Ones(M);
        for (int i = M / 2 + 1; i < M; ++i) {
            v[i] = 1 + epsilon;
        }
        Eigen::VectorXd nu = v * (dt / dx);

        Eigen::VectorXd main_diag_value = Eigen::VectorXd::Constant(M, 1) + nu;
        Eigen::VectorXd sub_diag_value = -nu.tail(M - 1);

        Eigen::SparseMatrix<double> A(M, M);
        for (int i = 0; i < M; ++i) {
            A.insert(i, i) = main_diag_value[i];
            if (i < M - 1) {
                A.insert(i, i + 1) = sub_diag_value[i];
            }
        }
        A.makeCompressed();
        return A;
    }

    std::vector<double> get_p_hat(int n) {
        return p[n];
    }

    void update_p() {
        p[0][0] = BC;
        for (int j = 1; j < M; ++j) {
            p[0][j] = IC;
        }

        for (int n = 0; n < N - 1; ++n) {
            std::vector<double> rhs = get_p_hat(n + 1);
            for (int j = 0; j < M; ++j) {
                rhs[j] += p[n][j];
            }
            Eigen::SparseMatrix<double> A = get_coefficient_m_standard();
            Eigen::VectorXd solution = Eigen::SparseLU<Eigen::SparseMatrix<double>>(A).solve(Eigen::VectorXd::Map(rhs.data(), rhs.size()));
            for (int j = 0; j < M; ++j) {
                p[n + 1][j] = solution[j];
            }
        }
    }
};

class FilteredImplicit : public Implicit {
public:
    FilteredImplicit(double dx, double BC, double IC, double gamma, double epsilon) 
        : Implicit(dx, BC, IC, gamma, epsilon) {}

    std::string toString() const {
        return "Filtered_Implicit";
    }

    Eigen::SparseMatrix<double> get_coefficient_m_filtered() {
        Eigen::VectorXd v = Eigen::VectorXd::Ones(M);
        for (int i = M / 2 + 1; i < M; ++i) {
            v[i] = 1 + epsilon;
        }
        Eigen::VectorXd nu = v * (dt / dx);

        Eigen::VectorXd main_diag = (2 / (2 - gamma)) + nu;
        Eigen::VectorXd sub_diag = -nu.tail(M - 1);
        Eigen::SparseMatrix<double> A(M, M);
        for (int i = 0; i < M; ++i) {
            A.insert(i, i) = main_diag[i];
            if (i < M - 1) {
                A.insert(i, i + 1) = sub_diag[i];
            }
        }
        A.makeCompressed();
        return A;
    }

    void update_p() {
        for (int j = 0; j < M; ++j) {
            p[0][j] = BC;  // set matrix boundary condition
        }
        for (int j = 1; j < M; ++j) {
            p[0][j] = IC;
        }
        double nu = dt / dx;

        std::vector<double> rhs = get_p_hat(1);
        for (int j = 0; j < M; ++j) {
            rhs[j] += p[0][j];
        }
        Eigen::SparseMatrix<double> A = get_coefficient_m_standard();
        Eigen::VectorXd solution = Eigen::SparseLU<Eigen::SparseMatrix<double>>(A).solve(Eigen::VectorXd::Map(rhs.data(), rhs.size()));
        for (int j = 0; j < M; ++j) {
            p[1][j] = solution[j];
        }

        if (gamma == 0) {
            Implicit::update_p();
        } else {
            for (int n = 1; n < N - 1; ++n) {
                rhs = get_p_hat(n + 1);
                for (int j = 0; j < M; ++j) {
                    rhs[j] = (nu * rhs[j]) + ((1 + ((2 * gamma) / (2 - gamma))) * p[n][j]) - ((gamma / (2 - gamma)) * p[n - 1][j]);
                }
                Eigen::SparseMatrix<double> A = get_coefficient_m_filtered();
                Eigen::VectorXd solution = Eigen::SparseLU<Eigen::SparseMatrix<double>>(A).solve(Eigen::VectorXd::Map(rhs.data(), rhs.size()));
                for (int j = 0; j < M; ++j) {
                    p[n + 1][j] = solution[j];
                }
            }
        }
    }
};

std::vector<double> rate_of_convergence(const std::vector<std::vector<double>>& error_table) {
    std::vector<double> rates;
    for (size_t i = 1; i < error_table.size(); ++i) {
        double dx1 = error_table[i - 1][0];
        double dx2 = error_table[i][0];
        double error1 = error_table[i - 1].back();
        double error2 = error_table[i].back();
        double rate = std::log(error1 / error2) / std::log(dx1 / dx2);
        rates.push_back(rate);
    }
    return rates;
}

std::vector<double> density_check(const Exact& s, double tolerance = 1e-3, int n = 0) {
    std::vector<double> results;
    std::vector<bool> matches(s.get_p().size(), false); // assuming get_p() returns the density array
    for (size_t i = 0; i < s.get_p().size(); ++i) {
        matches[i] = std::fabs(s.get_p()[i] - s.BC) < tolerance;
    }
    int t_time_level = -1;
    for (size_t i = 0; i < matches.size(); ++i) {
        if (matches[i]) {
            t_time_level = static_cast<int>(i);
            break;
        }
    }

    double true_ATT = (epsilon != 0) ? 0.5 + (n * s.dt) + (1 / (1 + s.epsilon)) * (1 - 0.5) : 1;

    int m_time_level = std::distance(s.get_p().begin(), std::max_element(s.get_p().begin(), s.get_p().end()));

    double m_est_ATT = m_time_level * s.dt;
    double t_est_ATT = t_time_level * s.dt;
    double t_error = t_est_ATT - true_ATT;
    double m_error = m_est_ATT - true_ATT;

    results.push_back(s.dt);
    results.push_back(true_ATT);
    results.push_back(t_error);
    results.push_back(t_time_level);
    results.push_back(t_est_ATT);
    results.push_back(m_error);
    results.push_back(m_time_level);
    results.push_back(m_est_ATT);
    return results;
}

std::vector<double> error(const Exact& approx, const Exact& exact, const std::vector<double>& tvalues = {0, 0.2, 0.4, 0.6, 0.8, 1}) {
    std::vector<double> tval_errors;
    std::vector<double> t(approx.N);
    for (int i = 0; i < approx.N; ++i) {
        t[i] = i * approx.dt;
    }

    for (double t_val : tvalues) {
        auto it = std::min_element(t.begin(), t.end(), [t_val](double a, double b) {
            return std::fabs(a - t_val) < std::fabs(b - t_val);
        });
        int n = std::distance(t.begin(), it);
        std::vector<double> error(approx.M);
        for (int j = 0; j < approx.M; ++j) {
            error[j] = std::fabs(approx.p[n][j] - exact.p[n][j]);
        }
        tval_errors.push_back(std::accumulate(error.begin(), error.end(), 0.0) * exact.dx);
    }
    return tval_errors;
}