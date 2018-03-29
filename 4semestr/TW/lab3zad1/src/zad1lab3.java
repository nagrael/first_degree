
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class zad1lab3 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		int M = 30;
		int n1 = 1;
		int n2 = 1;
	     int p1 = 50;
	     int p2 = 50;
	     if (n1*p1 != n2*p2){
	    	 throw new WrongParametsException("Number of goods produced " +
	                    "is not equal with number of goods consumed. Check the params!");
	     }
		// TODO Auto-generated method stub
		Buffer buffer = new Buffer(M);
		ExecutorService service = Executors.newFixedThreadPool(n1 + n2);
        for(int i=1; i<=n1; i++) {
            service.submit(new Producer(buffer,p1,M));
        }

        for(int i=1; i<=n2; i++) {
            service.submit(new Consumer(buffer,p2,M));
        }
        service.shutdown();
        try {
			service.awaitTermination(2L,TimeUnit.SECONDS);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        	
        if(buffer.Empty())
        	System.out.println("Empty");
        else
        	System.out.println("Not Empty");
	}

}
