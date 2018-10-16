package com.delta;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.Session;
import org.apache.commons.math3.util.Precision;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Random;

public class FillFlightData {
    static private Session session;
    static private Cluster cluster;
    static private ArrayList<String> setFlights;
    static private Random rand = new Random();

    private static void initFlights() {
        final String selectCQL = "SELECT flight_number FROM counter_reservations";
        ResultSet rs = session.execute(selectCQL);
        setFlights = new ArrayList<String>();
        for (Row row : rs) {
            setFlights.add(row.getString("flight_number"));
        }
    }

    static {
        String serverIp = "127.0.0.1";
        String keyspace = "avia";
        cluster = Cluster.builder()
                .addContactPoints(serverIp)
                .build();
        session = cluster.connect(keyspace);
    }

    private static long getRandomDate() {
        DateFormat dateFormat = new SimpleDateFormat("yyyy");
        try {
            long timestampFrom = dateFormat.parse("2008").getTime();
            long timestampTo = dateFormat.parse("2018").getTime();
            return timestampFrom + (long) (rand.nextDouble() * (timestampTo - timestampFrom));
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return 0;
    }

    public static void main(String[] args) {
        initFlights();
        final String insertCQL = "INSERT INTO flight_data (time, flight_number, speed, height, remaining_distance, " +
                "temperature_overboard, engine_condition, weather_condition) " +
                "VALUES (%s, '%s', %s, %s, %s, %s, '%s', '%s')";

        final String[] engineConditions = new String[]{"good", "normal", "bad", "trouble"};
        final String[] weatherConditions = new String[]{"sunny", "cloudy", "rainy", "foggy"};
        int n = args.length > 0 ? Integer.parseInt(args[0]) : 1;
        for (int i = 0; i < n; i++) {
            session.execute(String.format(insertCQL,
                    getRandomDate(),
                    setFlights.get(rand.nextInt(setFlights.size())),
                    Precision.round(rand.nextDouble() * 1001, 2),
                    Precision.round(rand.nextDouble() * 10001, 2),
                    Precision.round(rand.nextDouble() * 10000, 2),
                    Precision.round(-(rand.nextDouble() * 70) - 30, 2),
                    engineConditions[rand.nextInt(engineConditions.length)],
                    weatherConditions[rand.nextInt(weatherConditions.length)]));
        }
        cluster.close();
    }
}
