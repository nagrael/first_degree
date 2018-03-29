package laboratory.server;

/**
 * Created by Jan on 2017-05-07.
 */
import Ice.Current;
import Ice.Identity;
import lab._EquipmentDisp;

public class EquipmentImp extends _EquipmentDisp {


    @Override
    public int use(Current __current) {
        return 0;
    }

    @Override
    public int stopuse(Current __current) {
        return 0;
    }

    @Override
    public void addClient(Identity ident, Current __current) {

    }

    @Override
    public void removeClient(Identity ident, Current __current) {

    }
}
