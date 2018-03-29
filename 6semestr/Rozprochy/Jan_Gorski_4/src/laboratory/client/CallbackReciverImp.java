package laboratory.client;

import Ice.Current;
import lab._CallbackReceiverDisp;

/**
 * Created by Jan on 2017-05-07.
 */
public class CallbackReciverImp extends _CallbackReceiverDisp {
    @Override
    public void callback(String msg, Current __current) {
            System.out.println("received callback: " + msg);
    }
}
