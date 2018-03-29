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

public final class CallbackReceiverHolder extends Ice.ObjectHolderBase<CallbackReceiver>
{
    public
    CallbackReceiverHolder()
    {
    }

    public
    CallbackReceiverHolder(CallbackReceiver value)
    {
        this.value = value;
    }

    public void
    patch(Ice.Object v)
    {
        if(v == null || v instanceof CallbackReceiver)
        {
            value = (CallbackReceiver)v;
        }
        else
        {
            IceInternal.Ex.throwUOE(type(), v);
        }
    }

    public String
    type()
    {
        return _CallbackReceiverDisp.ice_staticId();
    }
}
