package laboratory.server;

import Ice.Identity;
import lab.Equipment;
import lab.ListAdap;

import java.util.*;

/**
 * Created by Jan on 2017-05-07.
 */
public class Server  {

    public  void t1 ( String[] args)
    {
        int status = 0;
        final String[] catname = {"Camera", "Telescope"};
        int N = 3;
        Ice.Communicator communicator = null;
        ArrayList<Thread> tlist = new ArrayList<>();
        ArrayList<CamImpl> clist = new ArrayList<>();
        ArrayList<TeleImpl> telist = new ArrayList<>();
        try
        {
            // 1. Inicjalizacja ICE - utworzenie communicatora
            communicator = Ice.Util.initialize(args);

            // 2. Konfiguracja adaptera
            // METODA 1 (polecana produkcyjnie): Konfiguracja adaptera Adapter1 jest w pliku konfiguracyjnym podanym jako parametr uruchomienia serwera
            //Ice.ObjectAdapter adapter = communicator.createObjectAdapter("Adapter1");

            // METODA 2 (niepolecana, dopuszczalna testowo): Konfiguracja adaptera Adapter1 jest w kodzie źródłowym
            Ice.ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("Adapter1", "tcp -h localhost -p 10000:udp -h localhost -p 10000");

            // 3. Stworzenie serwanta/serwantów
            Map<String,List<String>> lists = new HashMap<>();

            Equipment eqServant1;

            // 4. Dodanie wpisów do tablicy ASM
            ArrayList<String> tmp = new ArrayList<>();

            for(String cate: catname) {
                for (int i = 1; i<=N; i++) {
                    tmp.add(cate+i);
                    if(cate =="Telescope"){
                        eqServant1 = new TeleImpl(communicator);
                        telist.add((TeleImpl)eqServant1);
                        Thread t = new Thread((TeleImpl)eqServant1);
                        tlist.add(t);
                        t.start();
                    }
                    else {
                        eqServant1 = new CamImpl(communicator);
                        clist.add((CamImpl)eqServant1);
                        Thread t = new Thread((CamImpl)eqServant1);
                        tlist.add(t);
                        t.start();
                    }

                    adapter.add(eqServant1, new Identity(cate+i, cate));
                }
                lists.put(cate,tmp);
                tmp = new ArrayList<>();
            }
//            adapter.add(eqServant2, new Identity("Camera22", "Camera"));
//            adapter.add(eqServant1, new Identity("Telescope11", "Telescope"));
//            adapter.add(eqServant2, new Identity("Telescope22", "Telescope"));
//            //adapter.add(eqlcServant2, new Identity("calc22", "calc"));
//
//            tmp.add("Camera11");
//            tmp.add("Camera22");
//            lists.put("Camera",tmp );
            ListAdapImp alist = new ListAdapImp(lists);
            adapter.add(alist, new Identity("eqlist", "list"));
            // 5. Aktywacja adaptera i przejście w pętlę przetwarzania żądań
            adapter.activate();

            System.out.println("Entering event processing loop...");

            communicator.waitForShutdown();

        }
        catch (Exception e)
        {
            System.err.println(e);
            status = 1;
        }
        finally {
            for (CamImpl x : clist){
                x.destroy();
            }
            for (TeleImpl x: telist){
                x.destroy();
            }
            for (Thread x: tlist){
                try {
                    x.join();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
        if (communicator != null)
        {
            // Clean up
            //
            try
            {
                communicator.destroy();
            }
            catch (Exception e)
            {
                System.err.println(e);
                status = 1;
            }
        }
        System.exit(status);
    }


    public static void main(String[] args)
    {
        Server app = new Server();
        app.t1(args);

    }
}
