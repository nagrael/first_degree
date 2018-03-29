// **********************************************************************
//
// Copyright (c) 2003-2016 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************
//
// Ice version 3.6.3
//
// <auto-generated>
//
// Generated from file `lab.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

package lab;

/**
 * Provides type-specific helper functions.
 **/
public final class ListAdapPrxHelper extends Ice.ObjectPrxHelperBase implements ListAdapPrx
{
    private static final String __all_name = "all";

    public String[] all()
    {
        return all(null, false);
    }

    public String[] all(java.util.Map<String, String> __ctx)
    {
        return all(__ctx, true);
    }

    private String[] all(java.util.Map<String, String> __ctx, boolean __explicitCtx)
    {
        __checkTwowayOnly(__all_name);
        return end_all(begin_all(__ctx, __explicitCtx, true, null));
    }

    public Ice.AsyncResult begin_all()
    {
        return begin_all(null, false, false, null);
    }

    public Ice.AsyncResult begin_all(java.util.Map<String, String> __ctx)
    {
        return begin_all(__ctx, true, false, null);
    }

    public Ice.AsyncResult begin_all(Ice.Callback __cb)
    {
        return begin_all(null, false, false, __cb);
    }

    public Ice.AsyncResult begin_all(java.util.Map<String, String> __ctx, Ice.Callback __cb)
    {
        return begin_all(__ctx, true, false, __cb);
    }

    public Ice.AsyncResult begin_all(Callback_ListAdap_all __cb)
    {
        return begin_all(null, false, false, __cb);
    }

    public Ice.AsyncResult begin_all(java.util.Map<String, String> __ctx, Callback_ListAdap_all __cb)
    {
        return begin_all(__ctx, true, false, __cb);
    }

    public Ice.AsyncResult begin_all(IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                     IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb)
    {
        return begin_all(null, false, false, __responseCb, __exceptionCb, null);
    }

    public Ice.AsyncResult begin_all(IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                     IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                     IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_all(null, false, false, __responseCb, __exceptionCb, __sentCb);
    }

    public Ice.AsyncResult begin_all(java.util.Map<String, String> __ctx, 
                                     IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                     IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb)
    {
        return begin_all(__ctx, true, false, __responseCb, __exceptionCb, null);
    }

    public Ice.AsyncResult begin_all(java.util.Map<String, String> __ctx, 
                                     IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                     IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                     IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_all(__ctx, true, false, __responseCb, __exceptionCb, __sentCb);
    }

    private Ice.AsyncResult begin_all(java.util.Map<String, String> __ctx, 
                                      boolean __explicitCtx, 
                                      boolean __synchronous, 
                                      IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                      IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_all(__ctx, __explicitCtx, __synchronous, 
                         new IceInternal.Functional_TwowayCallbackArg1<String[]>(__responseCb, __exceptionCb, __sentCb)
                             {
                                 public final void __completed(Ice.AsyncResult __result)
                                 {
                                     ListAdapPrxHelper.__all_completed(this, __result);
                                 }
                             });
    }

    private Ice.AsyncResult begin_all(java.util.Map<String, String> __ctx, 
                                      boolean __explicitCtx, 
                                      boolean __synchronous, 
                                      IceInternal.CallbackBase __cb)
    {
        __checkAsyncTwowayOnly(__all_name);
        IceInternal.OutgoingAsync __result = getOutgoingAsync(__all_name, __cb);
        try
        {
            __result.prepare(__all_name, Ice.OperationMode.Normal, __ctx, __explicitCtx, __synchronous);
            __result.writeEmptyParams();
            __result.invoke();
        }
        catch(Ice.Exception __ex)
        {
            __result.abort(__ex);
        }
        return __result;
    }

    public String[] end_all(Ice.AsyncResult __iresult)
    {
        IceInternal.OutgoingAsync __result = IceInternal.OutgoingAsync.check(__iresult, this, __all_name);
        try
        {
            if(!__result.__wait())
            {
                try
                {
                    __result.throwUserException();
                }
                catch(Ice.UserException __ex)
                {
                    throw new Ice.UnknownUserException(__ex.ice_name(), __ex);
                }
            }
            IceInternal.BasicStream __is = __result.startReadParams();
            String[] __ret;
            __ret = seqHelper.read(__is);
            __result.endReadParams();
            return __ret;
        }
        finally
        {
            if(__result != null)
            {
                __result.cacheMessageBuffers();
            }
        }
    }

    static public void __all_completed(Ice.TwowayCallbackArg1<String[]> __cb, Ice.AsyncResult __result)
    {
        lab.ListAdapPrx __proxy = (lab.ListAdapPrx)__result.getProxy();
        String[] __ret = null;
        try
        {
            __ret = __proxy.end_all(__result);
        }
        catch(Ice.LocalException __ex)
        {
            __cb.exception(__ex);
            return;
        }
        catch(Ice.SystemException __ex)
        {
            __cb.exception(__ex);
            return;
        }
        __cb.response(__ret);
    }

    private static final String __allbycategory_name = "allbycategory";

    public String[] allbycategory(String name)
    {
        return allbycategory(name, null, false);
    }

    public String[] allbycategory(String name, java.util.Map<String, String> __ctx)
    {
        return allbycategory(name, __ctx, true);
    }

    private String[] allbycategory(String name, java.util.Map<String, String> __ctx, boolean __explicitCtx)
    {
        __checkTwowayOnly(__allbycategory_name);
        return end_allbycategory(begin_allbycategory(name, __ctx, __explicitCtx, true, null));
    }

    public Ice.AsyncResult begin_allbycategory(String name)
    {
        return begin_allbycategory(name, null, false, false, null);
    }

    public Ice.AsyncResult begin_allbycategory(String name, java.util.Map<String, String> __ctx)
    {
        return begin_allbycategory(name, __ctx, true, false, null);
    }

    public Ice.AsyncResult begin_allbycategory(String name, Ice.Callback __cb)
    {
        return begin_allbycategory(name, null, false, false, __cb);
    }

    public Ice.AsyncResult begin_allbycategory(String name, java.util.Map<String, String> __ctx, Ice.Callback __cb)
    {
        return begin_allbycategory(name, __ctx, true, false, __cb);
    }

    public Ice.AsyncResult begin_allbycategory(String name, Callback_ListAdap_allbycategory __cb)
    {
        return begin_allbycategory(name, null, false, false, __cb);
    }

    public Ice.AsyncResult begin_allbycategory(String name, java.util.Map<String, String> __ctx, Callback_ListAdap_allbycategory __cb)
    {
        return begin_allbycategory(name, __ctx, true, false, __cb);
    }

    public Ice.AsyncResult begin_allbycategory(String name, 
                                               IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                               IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb)
    {
        return begin_allbycategory(name, null, false, false, __responseCb, __exceptionCb, null);
    }

    public Ice.AsyncResult begin_allbycategory(String name, 
                                               IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                               IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                               IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_allbycategory(name, null, false, false, __responseCb, __exceptionCb, __sentCb);
    }

    public Ice.AsyncResult begin_allbycategory(String name, 
                                               java.util.Map<String, String> __ctx, 
                                               IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                               IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb)
    {
        return begin_allbycategory(name, __ctx, true, false, __responseCb, __exceptionCb, null);
    }

    public Ice.AsyncResult begin_allbycategory(String name, 
                                               java.util.Map<String, String> __ctx, 
                                               IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                               IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                               IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_allbycategory(name, __ctx, true, false, __responseCb, __exceptionCb, __sentCb);
    }

    private Ice.AsyncResult begin_allbycategory(String name, 
                                                java.util.Map<String, String> __ctx, 
                                                boolean __explicitCtx, 
                                                boolean __synchronous, 
                                                IceInternal.Functional_GenericCallback1<String[]> __responseCb, 
                                                IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                                IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_allbycategory(name, __ctx, __explicitCtx, __synchronous, 
                                   new IceInternal.Functional_TwowayCallbackArg1<String[]>(__responseCb, __exceptionCb, __sentCb)
                                       {
                                           public final void __completed(Ice.AsyncResult __result)
                                           {
                                               ListAdapPrxHelper.__allbycategory_completed(this, __result);
                                           }
                                       });
    }

    private Ice.AsyncResult begin_allbycategory(String name, 
                                                java.util.Map<String, String> __ctx, 
                                                boolean __explicitCtx, 
                                                boolean __synchronous, 
                                                IceInternal.CallbackBase __cb)
    {
        __checkAsyncTwowayOnly(__allbycategory_name);
        IceInternal.OutgoingAsync __result = getOutgoingAsync(__allbycategory_name, __cb);
        try
        {
            __result.prepare(__allbycategory_name, Ice.OperationMode.Normal, __ctx, __explicitCtx, __synchronous);
            IceInternal.BasicStream __os = __result.startWriteParams(Ice.FormatType.DefaultFormat);
            __os.writeString(name);
            __result.endWriteParams();
            __result.invoke();
        }
        catch(Ice.Exception __ex)
        {
            __result.abort(__ex);
        }
        return __result;
    }

    public String[] end_allbycategory(Ice.AsyncResult __iresult)
    {
        IceInternal.OutgoingAsync __result = IceInternal.OutgoingAsync.check(__iresult, this, __allbycategory_name);
        try
        {
            if(!__result.__wait())
            {
                try
                {
                    __result.throwUserException();
                }
                catch(Ice.UserException __ex)
                {
                    throw new Ice.UnknownUserException(__ex.ice_name(), __ex);
                }
            }
            IceInternal.BasicStream __is = __result.startReadParams();
            String[] __ret;
            __ret = seqHelper.read(__is);
            __result.endReadParams();
            return __ret;
        }
        finally
        {
            if(__result != null)
            {
                __result.cacheMessageBuffers();
            }
        }
    }

    static public void __allbycategory_completed(Ice.TwowayCallbackArg1<String[]> __cb, Ice.AsyncResult __result)
    {
        lab.ListAdapPrx __proxy = (lab.ListAdapPrx)__result.getProxy();
        String[] __ret = null;
        try
        {
            __ret = __proxy.end_allbycategory(__result);
        }
        catch(Ice.LocalException __ex)
        {
            __cb.exception(__ex);
            return;
        }
        catch(Ice.SystemException __ex)
        {
            __cb.exception(__ex);
            return;
        }
        __cb.response(__ret);
    }

    /**
     * Contacts the remote server to verify that the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param __obj The untyped proxy.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    public static ListAdapPrx checkedCast(Ice.ObjectPrx __obj)
    {
        return checkedCastImpl(__obj, ice_staticId(), ListAdapPrx.class, ListAdapPrxHelper.class);
    }

    /**
     * Contacts the remote server to verify that the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param __obj The untyped proxy.
     * @param __ctx The Context map to send with the invocation.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    public static ListAdapPrx checkedCast(Ice.ObjectPrx __obj, java.util.Map<String, String> __ctx)
    {
        return checkedCastImpl(__obj, __ctx, ice_staticId(), ListAdapPrx.class, ListAdapPrxHelper.class);
    }

    /**
     * Contacts the remote server to verify that a facet of the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param __obj The untyped proxy.
     * @param __facet The name of the desired facet.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    public static ListAdapPrx checkedCast(Ice.ObjectPrx __obj, String __facet)
    {
        return checkedCastImpl(__obj, __facet, ice_staticId(), ListAdapPrx.class, ListAdapPrxHelper.class);
    }

    /**
     * Contacts the remote server to verify that a facet of the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param __obj The untyped proxy.
     * @param __facet The name of the desired facet.
     * @param __ctx The Context map to send with the invocation.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    public static ListAdapPrx checkedCast(Ice.ObjectPrx __obj, String __facet, java.util.Map<String, String> __ctx)
    {
        return checkedCastImpl(__obj, __facet, __ctx, ice_staticId(), ListAdapPrx.class, ListAdapPrxHelper.class);
    }

    /**
     * Downcasts the given proxy to this type without contacting the remote server.
     * @param __obj The untyped proxy.
     * @return A proxy for this type.
     **/
    public static ListAdapPrx uncheckedCast(Ice.ObjectPrx __obj)
    {
        return uncheckedCastImpl(__obj, ListAdapPrx.class, ListAdapPrxHelper.class);
    }

    /**
     * Downcasts the given proxy to this type without contacting the remote server.
     * @param __obj The untyped proxy.
     * @param __facet The name of the desired facet.
     * @return A proxy for this type.
     **/
    public static ListAdapPrx uncheckedCast(Ice.ObjectPrx __obj, String __facet)
    {
        return uncheckedCastImpl(__obj, __facet, ListAdapPrx.class, ListAdapPrxHelper.class);
    }

    public static final String[] __ids =
    {
        "::Ice::Object",
        "::lab::ListAdap"
    };

    /**
     * Provides the Slice type ID of this type.
     * @return The Slice type ID.
     **/
    public static String ice_staticId()
    {
        return __ids[1];
    }

    public static void __write(IceInternal.BasicStream __os, ListAdapPrx v)
    {
        __os.writeProxy(v);
    }

    public static ListAdapPrx __read(IceInternal.BasicStream __is)
    {
        Ice.ObjectPrx proxy = __is.readProxy();
        if(proxy != null)
        {
            ListAdapPrxHelper result = new ListAdapPrxHelper();
            result.__copyFrom(proxy);
            return result;
        }
        return null;
    }

    public static final long serialVersionUID = 0L;
}
