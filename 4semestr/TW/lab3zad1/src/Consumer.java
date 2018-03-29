import java.util.Random;

class Consumer extends Thread {
	private Buffer buf;
	private int index;
	private int M;
	public Consumer(Buffer buf, int index, int M){
		this.buf = buf;
		this.index = index;
		this.M = M;
	}
	
	public void run() {
		Random rand = new Random();
	  	for (int i = 0; i < index; ++i) {
			int x = rand.nextInt(M/3)+1;
			System.out.println("comsumer" +x);
			buf.get(x);
			System.out.println("Consumer gets: " );
            i+=x;
        	try {
            	sleep((int) (Math.random() * 10));
        	} catch (InterruptedException e) {
            	System.out.println(e.getMessage());
        }		
	  }
	}
}
