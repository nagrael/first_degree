/**
 * ThingSpeak Appender for log4j Copyright 2014, Andrew Bythell
 * <abythell@ieee.org>
 * http://angryelectron.com
 *
 * The ThingSpeak Java Client is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or (at your
 * option) any later version.
 *
 * The ThingSpeak Java Client is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
 * Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * the ThingSpeak Appender. If not, see <http://www.gnu.org/licenses/>.
 */

package com.angryelectron.thingspeak.log4j;

import com.angryelectron.thingspeak.TestChannelSettings;
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.junit.BeforeClass;
import org.junit.Test;

/**
 * Test ThingSpeakAppender.
 */
public class ThingSpeakAppenderTest {
    
    /**
     * Credentials for a test ThingSpeak channel.
     */
    private final static Integer channelNumber = 15662;
    private final static String apiWriteKey = "I5X9EPC34LPX1HRP";
    
    public ThingSpeakAppenderTest() {
    }
    
    @BeforeClass
    public static void setUpClass() throws Exception {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
        Logger.getLogger("org.apache.http").setLevel(Level.OFF);
        pauseForAPIRateLimit();
    }
    
    private static void pauseForAPIRateLimit() throws InterruptedException {
        System.out.println("Waiting for rate limit to expire.");
        Thread.sleep(TestChannelSettings.rateLimit);
    }

    /**
     * Test of configureChannel method, of class ThingSpeakAppender.  To view the
     * logged data on ThingSpeak, visit https://thingspeak.com/channels/15662/feeds.     
     * @throws java.lang.InterruptedException
     */
    @Test
    public void testAppend() throws InterruptedException {
        System.out.println("testAppend");  
        ThingSpeakAppender appender = new ThingSpeakAppender();
        appender.configureChannel(channelNumber, apiWriteKey, null);
        appender.setThreshold(Level.INFO);
        appender.activateOptions();        
        Logger.getRootLogger().addAppender(appender);
        Logger.getLogger(this.getClass()).log(Level.INFO, "Test message from ThingSpeakAppender");
    }
}
