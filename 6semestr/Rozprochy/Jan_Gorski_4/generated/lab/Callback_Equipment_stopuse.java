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

public abstract class Callback_Equipment_stopuse
    extends IceInternal.TwowayCallback implements Ice.TwowayCallbackInt
{
    public final void __completed(Ice.AsyncResult __result)
    {
        EquipmentPrxHelper.__stopuse_completed(this, __result);
    }
}
