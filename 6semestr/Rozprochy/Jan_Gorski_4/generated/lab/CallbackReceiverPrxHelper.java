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
public final class CallbackReceiverPrxHelper extends Ice.ObjectPrxHelperBase implements CallbackReceiverPrx
{
    private static final String __callback_name = "callback";

    public void callback(String num)
    {
        callback(num, null, false);
    }

    public void callback(String num, java.util.Map<String, String> __ctx)
    {
        callback(num, __ctx, true);
    }

    private void callback(String num, java.util.Map<String, String> __ctx, boolean __explicitCtx)
    {
        end_callback(begin_callback(num, __ctx, __explicitCtx, true, null));
    }

    public Ice.AsyncResult begin_callback(String num)
    {
        return begin_callback(num, null, false, false, null);
    }

    public Ice.AsyncResult begin_callback(String num, java.util.Map<String, String> __ctx)
    {
        return begin_callback(num, __ctx, true, false, null);
    }

    public Ice.AsyncResult begin_callback(String num, Ice.Callback __cb)
    {
        return begin_callback(num, null, false, false, __cb);
    }

    public Ice.AsyncResult begin_callback(String num, java.util.Map<String, String> __ctx, Ice.Callback __cb)
    {
        return begin_callback(num, __ctx, true, false, __cb);
    }

    public Ice.AsyncResult begin_callback(String num, Callback_CallbackReceiver_callback __cb)
    {
        return begin_callback(num, null, false, false, __cb);
    }

    public Ice.AsyncResult begin_callback(String num, java.util.Map<String, String> __ctx, Callback_CallbackReceiver_callback __cb)
    {
        return begin_callback(num, __ctx, true, false, __cb);
    }

    public Ice.AsyncResult begin_callback(String num, 
                                          IceInternal.Functional_VoidCallback __responseCb, 
                                          IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb)
    {
        return begin_callback(num, null, false, false, __responseCb, __exceptionCb, null);
    }

    public Ice.AsyncResult begin_callback(String num, 
                                          IceInternal.Functional_VoidCallback __responseCb, 
                                          IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                          IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_callback(num, null, false, false, __responseCb, __exceptionCb, __sentCb);
    }

    public Ice.AsyncResult begin_callback(String num, 
                                          java.util.Map<String, String> __ctx, 
                                          IceInternal.Functional_VoidCallback __responseCb, 
                                          IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb)
    {
        return begin_callback(num, __ctx, true, false, __responseCb, __exceptionCb, null);
    }

    public Ice.AsyncResult begin_callback(String num, 
                                          java.util.Map<String, String> __ctx, 
                                          IceInternal.Functional_VoidCallback __responseCb, 
                                          IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                          IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_callback(num, __ctx, true, false, __responseCb, __exceptionCb, __sentCb);
    }

    private Ice.AsyncResult begin_callback(String num, 
                                           java.util.Map<String, String> __ctx, 
                                           boolean __explicitCtx, 
                                           boolean __synchronous, 
                                           IceInternal.Functional_VoidCallback __responseCb, 
                                           IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                           IceInternal.Functional_BoolCallback __sentCb)
    {
        return begin_callback(num, 
                              __ctx, 
                              __explicitCtx, 
                              __synchronous, 
                              new IceInternal.Functional_OnewayCallback(__responseCb, __exceptionCb, __sentCb));
    }

    private Ice.AsyncResult begin_callback(String num, 
                                           java.util.Map<String, String> __ctx, 
                                           boolean __explicitCtx, 
                                           boolean __synchronous, 
                                           IceInternal.CallbackBase __cb)
    {
        IceInternal.OutgoingAsync __result = getOutgoingAsync(__callback_name, __cb);
        try
        {
            __result.prepare(__callback_name, Ice.OperationMode.Normal, __ctx, __explicitCtx, __synchronous);
            IceInternal.BasicStream __os = __result.startWriteParams(Ice.FormatType.DefaultFormat);
            __os.writeString(num);
            __result.endWriteParams();
            __result.invoke();
        }
        catch(Ice.Exception __ex)
        {
            __result.abort(__ex);
        }
        return __result;
    }

    public void end_callback(Ice.AsyncResult __iresult)
    {
        __end(__iresult, __callback_name);
    }

    /**
     * Contacts the remote server to verify that the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param __obj The untyped proxy.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    public static CallbackReceiverPrx checkedCast(Ice.ObjectPrx __obj)
    {
        return checkedCastImpl(__obj, ice_staticId(), CallbackReceiverPrx.class, CallbackReceiverPrxHelper.class);
    }

    /**
     * Contacts the remote server to verify that the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param __obj The untyped proxy.
     * @param __ctx The Context map to send with the invocation.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    public static CallbackReceiverPrx checkedCast(Ice.ObjectPrx __obj, java.util.Map<String, String> __ctx)
    {
        return checkedCastImpl(__obj, __ctx, ice_staticId(), CallbackReceiverPrx.class, CallbackReceiverPrxHelper.class);
    }

    /**
     * Contacts the remote server to verify that a facet of the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param __obj The untyped proxy.
     * @param __facet The name of the desired facet.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    public static CallbackReceiverPrx checkedCast(Ice.ObjectPrx __obj, String __facet)
    {
        return checkedCastImpl(__obj, __facet, ice_staticId(), CallbackReceiverPrx.class, CallbackReceiverPrxHelper.class);
    }

    /**
     * Contacts the remote server to verify that a facet of the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param __obj The untyped proxy.
     * @param __facet The name of the desired facet.
     * @param __ctx The Context map to send with the invocation.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    public static CallbackReceiverPrx checkedCast(Ice.ObjectPrx __obj, String __facet, java.util.Map<String, String> __ctx)
    {
        return checkedCastImpl(__obj, __facet, __ctx, ice_staticId(), CallbackReceiverPrx.class, CallbackReceiverPrxHelper.class);
    }

    /**
     * Downcasts the given proxy to this type without contacting the remote server.
     * @param __obj The untyped proxy.
     * @return A proxy for this type.
     **/
    public static CallbackReceiverPrx uncheckedCast(Ice.ObjectPrx __obj)
    {
        return uncheckedCastImpl(__obj, CallbackReceiverPrx.class, CallbackReceiverPrxHelper.class);
    }

    /**
     * Downcasts the given proxy to this type without contacting the remote server.
     * @param __obj The untyped proxy.
     * @param __facet The name of the desired facet.
     * @return A proxy for this type.
     **/
    public static CallbackReceiverPrx uncheckedCast(Ice.ObjectPrx __obj, String __facet)
    {
        return uncheckedCastImpl(__obj, __facet, CallbackReceiverPrx.class, CallbackReceiverPrxHelper.class);
    }

    public static final String[] __ids =
    {
        "::Ice::Object",
        "::lab::CallbackReceiver"
    };

    /**
     * Provides the Slice type ID of this type.
     * @return The Slice type ID.
     **/
    public static String ice_staticId()
    {
        return __ids[1];
    }

    public static void __write(IceInternal.BasicStream __os, CallbackReceiverPrx v)
    {
        __os.writeProxy(v);
    }

    public static CallbackReceiverPrx __read(IceInternal.BasicStream __is)
    {
        Ice.ObjectPrx proxy = __is.readProxy();
        if(proxy != null)
        {
            CallbackReceiverPrxHelper result = new CallbackReceiverPrxHelper();
            result.__copyFrom(proxy);
            return result;
        }
        return null;
    }

    public static final long serialVersionUID = 0L;
}
