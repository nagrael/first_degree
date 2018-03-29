package agh.sr.zad6.zoo;


import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.ZooKeeper;


import java.util.Collections;



/**
 * Created by Jan on 2017-06-02.
 */
public class TreePrinter {


    private final ZooKeeper zooKeeper;

    public TreePrinter(ZooKeeper zooKeeper) {
        this.zooKeeper = zooKeeper;
    }

    public void startPrintingTree() {
        prettyTreePrint("/test_node",0);
    }

    private void prettyTreePrint(String zNode, int level) {
        System.out.println(StringForNode(zNode,level));
        try {
            zooKeeper.getChildren(zNode, false)
                    .forEach(child -> prettyTreePrint(zNode.concat("/" + child), level + 1));
        } catch (KeeperException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private String StringForNode(String zNodeName, int level) {
        StringBuffer st = new StringBuffer();
        st.append(String.join("", Collections.nCopies(level, "|")));
        st.append(zNodeName.substring(zNodeName.lastIndexOf("/")+1));
        return st.toString();
    }
}
