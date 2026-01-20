public class SimpleExceptionFlowModified{
    static class CustomException extends Exception {
    public CustomException (String msg){
            super(msg);
        }
    }
    public static void main(String[] args){
        try{
            B();
        } catch(CustomException e){
            System.out.println("Catch in main: " + e.getMessage());
        }

        try {
            A();
        } catch (CustomException e) {
            System.out.println("Catch in main: " + e.getMessage());
        }
    }
    public static void A()throws CustomException{
        try{
            throw new CustomException("Direct exception from A");
        } catch(CustomException e){
            System.out.println("Caught in A : " + e.getMessage());
            throw new CustomException ("From A");
        }finally{
            System.out.println("Finally in A");
        }
    }
    public static void B() throws CustomException{
        try{
            C();
        } catch(CustomException e){
            System.out.println("Caught in B : " + e.getMessage());
        throw new CustomException("From B");
        }
    }
    public static void C() throws CustomException{
        throw new CustomException("Thrown in C");
    }
}