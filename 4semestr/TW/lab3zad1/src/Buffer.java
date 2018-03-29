
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

class Buffer {
	private List<Integer> buffer = new ArrayList<Integer>();
	private int M;
	public Buffer(int M){
		this.M = 2*M;
	}
	public synchronized void put(int [] i) {
		while((M-buffer.size())< i.length) {
			try {
				wait();
				System.out.println("Producent waits");
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
			for(int j =0; j<i.length; ++j){
				buffer.add(i[j]);
				notify();
			}


  }
	public Boolean Empty(){
		return this.buffer.isEmpty();
	}
	public synchronized int get(int i) {
		while(buffer.size()<= i){
			try {
				wait();
				System.out.println("Consumer waits.");
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
		int val = 0;
		for( int j = 0; j<i;j++) {
			int tmp = new Random().nextInt(buffer.size());
			val = buffer.get(tmp);
			buffer.remove(tmp);
			notify();
			System.out.println("Consumer gets: "+val );
		}

		return val;
  }
}

