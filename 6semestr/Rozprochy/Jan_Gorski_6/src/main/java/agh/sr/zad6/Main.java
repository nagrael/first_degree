package agh.sr.zad6;

/**
 * Created by Jan on 2017-06-02.
 */
public class Main {
    public static void main(String[] args) {
        if(args.length < 2) System.exit(1);
        try{
            String exec[] = new String[args.length - 1];
            System.arraycopy(args, 1, exec, 0, exec.length);
            new Thread(new ZooKeeperClient(args[0], exec)).start();
        } catch (Exception e){
            e.printStackTrace();
        }
    }


}
