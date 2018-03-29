package laboratory.client;

import Ice.AsyncResult;
import lab.*;
import laboratory.server.CamImpl;
import laboratory.server.EquipmentImp;
import laboratory.server.TeleImpl;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

/**
 * Created by Jan on 2017-05-07.
 */
public class Client {
    static Ice.Communicator communicator = null;
    public static void main(String[] args)
    {
        int status = 0;


        try {
            // 1. Inicjalizacja ICE
            communicator = Ice.Util.initialize(args);

            // 2. Uzyskanie referencji obiektu na podstawie linii w pliku konfiguracyjnym
            //Ice.ObjectPrx base = communicator.propertyToProxy("Calc1.Proxy");
            // 2. To samo co powy�ej, ale mniej �adnie
            Ice.ObjectPrx base = communicator.stringToProxy("list/eqlist:tcp -h localhost -p 10000:udp -h localhost -p 10000");

            // 3. Rzutowanie, zaw�anie
            ListAdapPrx lists = ListAdapPrxHelper.checkedCast(base);
            if (lists == null) throw new Error("Invalid proxy");
            java.io.BufferedReader in = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));
            EquipmentPrx obj = new Client().choose(lists);
            // 4. Wywolanie zdalnych operacji
            Ice.ObjectAdapter adapter = communicator.createObjectAdapter("");
            Ice.Identity ident = new Ice.Identity();
            ident.name = java.util.UUID.randomUUID().toString();
            ident.category = "";
            adapter.add(new CallbackReciverImp(), ident);
            adapter.activate();

            //obj.addClient(ident);

            String line = null;

            AsyncResult ar = null;
            do
            {
                try
                {
                    System.out.print("==> ");
                    System.out.flush();
                    line = in.readLine();
                    if (line == null)
                    {
                        break;
                    }
                    if (line.equals("a"))
                    {
                        int r = obj.use();
                        System.out.println("RESULT = " + r);
                    }
                    if (line.equals("b"))
                    {
                        if(obj instanceof CamPrx) {
                            int r = ((CamPrx) obj).setangle(1, 2, 3);
                            System.out.println("RESULT = " + r);
                        }
                    }
                    if (line.equals("bb"))
                    {
                        if(obj instanceof TelePrx) {
                            int r = ((TelePrx) obj).move(1, 2, 3);
                            System.out.println("RESULT = " + r);
                        }
                    }
                    if (line.equals("bbb"))
                    {
                        if(obj instanceof TelePrx) {
                            int r = ((TelePrx) obj).zoom(50);
                            System.out.println("RESULT = " + r);
                        }
                    }
                    if (line.equals("c"))
                    {
                        int r = obj.stopuse();
                        System.out.println("RESULT = " + r);
                    }
                    if (line.equals("d"))
                    {
                        obj.removeClient(ident);

                    }
                    if (line.equals("e"))
                    {

                        obj.ice_getConnection().setAdapter(adapter);
                        obj.addClient(ident);

                    }
                    if (line.equals("f"))
                    {
                        obj = new  Client().choose(lists);


                    }
                    else if (line.equals("x"))
                    {
                        // Nothing to do
                    }
                }
                catch (java.io.IOException ex)
                {
                    System.err.println(ex);
                }
            }
            while (!line.equals("x"));
            communicator.waitForShutdown();

        } catch (Ice.LocalException e) {
            e.printStackTrace();
            status = 1;
        } catch (Exception e) {
            System.err.println(e.getMessage());
            status = 1;
        }
        if (communicator != null) {
            // Clean up
            //
            try {
                communicator.destroy();
            } catch (Exception e) {
                System.err.println(e.getMessage());
                status = 1;
            }
        }
        System.exit(status);
    }

    EquipmentPrx choose(ListAdapPrx lists) throws IOException {
        String [] a = lists.all();
        List<String > lista = Arrays.asList(a);
        String tmp = "";
        java.io.BufferedReader in = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));
        do {
            System.out.println("Choose equipment");
            for (String x : lista) {
                System.out.println(x);
            }

            tmp = in.readLine();
        }while (!lista.contains(tmp));
        a = lists.allbycategory(tmp);
        lista = Arrays.asList(a);
        String tmp1 = "";
        do {
            System.out.println("Choose specific equipment");
            for (String x : lista) {
                System.out.println(x);
            }

            tmp1 = in.readLine();
        }while (!lista.contains(tmp1));
        Ice.ObjectPrx base1 = communicator.stringToProxy(tmp+"/"+tmp1+":tcp -h localhost -p 10000:udp -h localhost -p 10000");

        // 3. Rzutowanie, zaw�anie
        return  CamPrxHelper.checkedCast(base1);
    }

}
