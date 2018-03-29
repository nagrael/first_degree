
#ifndef LAB_ICE
#define LAB_ICE

#include <C:\Program Files (x86)\ZeroC\Ice-3.6.3\slice\Ice\Identity.ice>
module lab
{

    interface CallbackReceiver
    {
        void callback(string num);
    };


  interface Equipment
  {
    int use();
    int stopuse();
    void addClient(Ice::Identity ident);
    void removeClient(Ice::Identity ident);

  };

      sequence<string> seq;

      interface ListAdap
      {
          seq all();
          seq allbycategory(string name);
      };

  interface Cam extends Equipment
  {
    int setangle(int x, int y, int z);

  };

    interface Tele extends Equipment
    {
       int move(int x, int y, int z);
       int zoom(int zo);

    };
};

#endif
