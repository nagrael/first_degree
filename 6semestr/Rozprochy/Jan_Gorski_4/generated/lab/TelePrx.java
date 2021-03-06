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

public interface TelePrx extends EquipmentPrx
{
    public int move(int x, int y, int z);

    public int move(int x, int y, int z, java.util.Map<String, String> __ctx);

    public Ice.AsyncResult begin_move(int x, int y, int z);

    public Ice.AsyncResult begin_move(int x, int y, int z, java.util.Map<String, String> __ctx);

    public Ice.AsyncResult begin_move(int x, int y, int z, Ice.Callback __cb);

    public Ice.AsyncResult begin_move(int x, int y, int z, java.util.Map<String, String> __ctx, Ice.Callback __cb);

    public Ice.AsyncResult begin_move(int x, int y, int z, Callback_Tele_move __cb);

    public Ice.AsyncResult begin_move(int x, int y, int z, java.util.Map<String, String> __ctx, Callback_Tele_move __cb);

    public Ice.AsyncResult begin_move(int x, 
                                      int y, 
                                      int z, 
                                      IceInternal.Functional_IntCallback __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb);

    public Ice.AsyncResult begin_move(int x, 
                                      int y, 
                                      int z, 
                                      IceInternal.Functional_IntCallback __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                      IceInternal.Functional_BoolCallback __sentCb);

    public Ice.AsyncResult begin_move(int x, 
                                      int y, 
                                      int z, 
                                      java.util.Map<String, String> __ctx, 
                                      IceInternal.Functional_IntCallback __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb);

    public Ice.AsyncResult begin_move(int x, 
                                      int y, 
                                      int z, 
                                      java.util.Map<String, String> __ctx, 
                                      IceInternal.Functional_IntCallback __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                      IceInternal.Functional_BoolCallback __sentCb);

    public int end_move(Ice.AsyncResult __result);

    public int zoom(int zo);

    public int zoom(int zo, java.util.Map<String, String> __ctx);

    public Ice.AsyncResult begin_zoom(int zo);

    public Ice.AsyncResult begin_zoom(int zo, java.util.Map<String, String> __ctx);

    public Ice.AsyncResult begin_zoom(int zo, Ice.Callback __cb);

    public Ice.AsyncResult begin_zoom(int zo, java.util.Map<String, String> __ctx, Ice.Callback __cb);

    public Ice.AsyncResult begin_zoom(int zo, Callback_Tele_zoom __cb);

    public Ice.AsyncResult begin_zoom(int zo, java.util.Map<String, String> __ctx, Callback_Tele_zoom __cb);

    public Ice.AsyncResult begin_zoom(int zo, 
                                      IceInternal.Functional_IntCallback __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb);

    public Ice.AsyncResult begin_zoom(int zo, 
                                      IceInternal.Functional_IntCallback __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                      IceInternal.Functional_BoolCallback __sentCb);

    public Ice.AsyncResult begin_zoom(int zo, 
                                      java.util.Map<String, String> __ctx, 
                                      IceInternal.Functional_IntCallback __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb);

    public Ice.AsyncResult begin_zoom(int zo, 
                                      java.util.Map<String, String> __ctx, 
                                      IceInternal.Functional_IntCallback __responseCb, 
                                      IceInternal.Functional_GenericCallback1<Ice.Exception> __exceptionCb, 
                                      IceInternal.Functional_BoolCallback __sentCb);

    public int end_zoom(Ice.AsyncResult __result);
}
