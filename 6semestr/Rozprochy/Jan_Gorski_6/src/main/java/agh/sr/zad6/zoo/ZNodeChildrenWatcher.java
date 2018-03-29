package agh.sr.zad6.zoo;

import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;


/**
 * Created by Jan on 2017-06-02.
 */
public class ZNodeChildrenWatcher implements Watcher {

    private final ZooKeeper zooKeeper;

    public ZNodeChildrenWatcher(ZooKeeper zooKeeper) {
        this.zooKeeper = zooKeeper;
    }

    public void process(WatchedEvent watchedEvent) {
        try {
            this.zooKeeper.getChildren("/test_node", this);
            countingDescendants();
        } catch (KeeperException e) {
            e.getCause();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private void countingDescendants() throws KeeperException, InterruptedException {
        Stat stat = this.zooKeeper.exists("/test_node", false);
        if(stat!=null){
            int descendants = this.zooKeeper.getChildren("/test_node", false).size();
            System.out.println(descendants);
        }
    }

}
