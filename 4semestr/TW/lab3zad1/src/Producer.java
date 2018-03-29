import java.util.Random;

class Producer extends Thread {
	private Buffer buf;
	private int index;
	private int M;
	public Producer(Buffer buf, int index, int M){
		this.buf = buf;
		this.index = index;
		this.M = M;
	}

	public void run() {
		Random x = new Random();
	  for (int i = 0; i < index; ++i) {
		  int j = x.nextInt(M/3)+1;
		  System.out.println(" producer" +j);
		  int a[] = new int[j];
		  for(int k =0; k<j ;++k){
			  a[k]= x.nextInt(index);
			  //System.out.println(a[k]);
		  }
          i+=j;
		  buf.put(a);
		  //System.out.println("Producer puts: " + a);
        try {
            sleep((int) (Math.random() * 10));
        } catch (InterruptedException e) {
            System.out.println(e.getMessage());
        }		
	  }
	}
}