package agh.sr.zad6;

import agh.sr.zad6.zoo.TreePrinter;
import agh.sr.zad6.zoo.ZNodeWatcher;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;

import java.util.Scanner;

/**
 * Created by Jan on 2017-06-02.
 */
public class ZooKeeperClient implements Runnable, Watcher {

    private final String hostAndPort;
    private final String[] exec;
    private final Scanner scanner = new Scanner(System.in);

    public ZooKeeperClient(String hostAndPort, String[] exec) {
        this.hostAndPort = hostAndPort;
        this.exec = exec;
    }

    public void run() {
        try {
            ZooKeeper zooKeeper = new ZooKeeper(hostAndPort, 10000, this);
            ZNodeWatcher zNodeWatcher = new ZNodeWatcher(zooKeeper, exec);
            TreePrinter treePrinter = new TreePrinter(zooKeeper);
            Stat stat = zooKeeper.exists("/test_node",zNodeWatcher);
            if(stat!=null) zNodeWatcher.handleExistingTestNode();
            printUsage();
            while(true){
                String cmd = scanner.nextLine();
                if(cmd.trim().equals("Q")) break;
                else if(cmd.trim().equals("T")){
                    treePrinter.startPrintingTree();
                }
                else {
                    printUsage();
                }
            }
        } catch (KeeperException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void process(WatchedEvent watchedEvent) {
        System.out.println(watchedEvent.toString());
    }

    private static void printUsage() {
        System.out.println("Possible command:");
        System.out.println("1. Q -> quit");
        System.out.println("2. T -> print tree like");
    }
}
