package laboratory.server;

import Ice.Connection;
import Ice.Current;
import Ice.Identity;
import lab.CallbackReceiverPrx;
import lab.CallbackReceiverPrxHelper;
import lab._TeleDisp;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * Created by Jan on 2017-05-08.
 */
public class TeleImpl extends _TeleDisp implements Runnable{
    private Ice.Communicator _communicator;
    private boolean _destroy = false;
    private boolean _chceck = false;
    private Map<Identity ,CallbackReceiverPrx> _clients = new HashMap<>();
    private LinkedList<String> _msg = new LinkedList<>();
    private Connection conn = null;

    @Override
    synchronized public int use(Current __current) {

        if(this.conn == null){
            this.conn = __current.con;
            return 0;
        }
        return -1;
    }

    @Override
    synchronized public int stopuse(Current __current) {
        if (this.conn != null) {

            if (this.conn == __current.con) {
                this.conn = null;
                return 0;
            }
        }
        return -1;
    }
    TeleImpl(Ice.Communicator communicator)
    {
        _communicator = communicator;
    }

    synchronized public void destroy()
    {
        System.out.println("destroying callback sender");
        _destroy = true;

        this.notify();
    }

    @Override
    synchronized public void addClient(Ice.Identity ident, Ice.Current current)
    {
        System.out.println("adding client `" + _communicator.identityToString(ident) + "'");

        Ice.ObjectPrx base = current.con.createProxy(ident);
        CallbackReceiverPrx client = CallbackReceiverPrxHelper.uncheckedCast(base);

        _clients.put(ident,client);
    }

    @Override
    synchronized public void removeClient(Identity ident, Current __current) {
        System.out.println("removing client `" + _communicator.identityToString(ident) + "'");
        _clients.remove(ident);
    }

    @Override
    public void run() {

        while (true) {
            Map<Identity ,CallbackReceiverPrx> clients;
            List<String> msgs;
            synchronized (this) {
                try {
                    this.wait(200000);
                } catch (java.lang.InterruptedException ex) {
                }
                if (_destroy) {
                    break;
                }
                if(_chceck){
                    conn=null;
                }
                _chceck =true;
                msgs = (List<String>)_msg.clone();
                _msg.clear();

                clients = new HashMap<>(_clients);
            }

            if (!clients.isEmpty()) {
                for (String msg : msgs) {
                    for (CallbackReceiverPrx p : clients.values()) {

                        try {
                            p.callback(msg);
                        } catch (Exception ex) {
                            System.out.println("removing client from Telescope `" + _communicator.identityToString(p.ice_getIdentity()) +
                                    "':");
                            ex.printStackTrace();

                            synchronized (this) {
                                _clients.remove(p.ice_getIdentity());
                            }
                        }
                    }
                }
            }
        }
    }


    @Override
    public int move(int x, int y, int z, Current __current) {
        if(this.conn == __current.con) {
            _msg.add("Telescope moved  x:" + x + ", y:" + y + ", z:" + z);
            System.out.println("Moved Telescope x:" + x + ", y:" + y + ", z:" + z);
            _chceck = false;
            notify();
            return 0;
        }
        return  -1;
    }

    @Override
    public int zoom(int zo, Current __current) {
        if(this.conn == __current.con) {
            _msg.add("Zoomed x:" + zo );
            System.out.println("Zoomed x:" + zo );
            _chceck = false;
            notify();
            return 0;
        }
        return  -1;
    }
}
