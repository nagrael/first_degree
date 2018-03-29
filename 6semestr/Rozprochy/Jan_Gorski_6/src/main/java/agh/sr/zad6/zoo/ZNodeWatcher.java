package agh.sr.zad6.zoo;

import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;

import java.io.IOException;


/**
 * Created by Jan on 2017-06-02.
 */
public class ZNodeWatcher implements Watcher {

    private final ZooKeeper zooKeeper;
    private final ZNodeChildrenWatcher ZNodeChildrenWatcher;
    private final String[] exec;
    private Process process = null;

    public ZNodeWatcher(final ZooKeeper zooKeeper, String[] exec) {
        addShutdownHookForProc(zooKeeper);
        this.zooKeeper = zooKeeper;
        ZNodeChildrenWatcher = new ZNodeChildrenWatcher(zooKeeper);
        this.exec = exec;
    }

    private void addShutdownHookForProc(final ZooKeeper zooKeeper) {
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            if(process!=null) process.destroy();
            try {
                zooKeeper.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }));
    }

    public void process(WatchedEvent watchedEvent) {
        try {
            zooKeeper.exists("/test_node", this);
            switch (watchedEvent.getType()) {
                case NodeCreated:
                    handleExistingTestNode();
                    break;
                case NodeDeleted:
                    System.out.println("Stopping exec...");
                    if (process != null) process.destroy();
                    break;
                default:
                    break;
            }
        } catch (KeeperException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void handleExistingTestNode() throws KeeperException, InterruptedException, IOException {
        zooKeeper.getChildren("/test_node", ZNodeChildrenWatcher);
        System.out.println("Starting exec...");
        process = Runtime.getRuntime().exec(exec);
    }


}
