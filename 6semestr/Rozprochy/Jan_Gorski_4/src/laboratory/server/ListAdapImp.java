package laboratory.server;

import Ice.Current;
import lab.Equipment;
import lab._ListAdapDisp;

import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Created by Jan on 2017-05-08.
 */
public class ListAdapImp extends _ListAdapDisp {
    private Map<String, List<String>> lista;

    public ListAdapImp(Map<String, List<String>> l){
        this.lista=l;
    }

    @Override
    public String[] all(Current __current) {
        Set<String> l = this.lista.keySet();
        return (String[]) l.toArray(new String[l.size()]);
    }

    @Override
    public String[] allbycategory(String name, Current __current) {
        List<String> l = this.lista.get(name);
        if(l!=null)
            return (String[]) l.toArray(new String[l.size()]);
        else
            return null;
    }
}
