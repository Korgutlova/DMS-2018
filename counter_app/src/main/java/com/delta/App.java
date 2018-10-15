package com.delta;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.Session;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;
import java.util.Random;

public class App {

    static private Random rand = new Random();
    static private Session session;
    static private Cluster cluster;
    static private ArrayList<String> setFlights;
    final static private String insertCQL = "INSERT INTO reservation (passenger, date, tickets) VALUES %s";
    final static private String updateCQL = "UPDATE counter_reservations SET amount_reservations = amount_reservations + %s WHERE flight_number = '%s'";
    final static private String exampleRow = "('%s', toTimeStamp(now()), [%s])";
    final static private String exampleTicket = "{type:'%s', place:'%s', price:%s, flight_number:'%s', passport_data:{email:'%s', first_name:'%s', last_name:'%s', third_name:'%s'}},";

    static {
        String serverIp = "127.0.0.1";
        String keyspace = "avia";
        cluster = Cluster.builder()
                .addContactPoints(serverIp)
                .build();
        session = cluster.connect(keyspace);
    }

    private static void initFlights() {
        final String selectCQL = "SELECT flight_number FROM counter_reservations";
        ResultSet rs = session.execute(selectCQL);
        setFlights = new ArrayList<String>();
        for (Row row : rs) {
            setFlights.add(row.getString("flight_number"));
        }
    }

    private static HashMap<String, Object> generateData() {
        HashMap<String, Object> customMap = new HashMap<String, Object>();
        StringBuilder stringBuilder = new StringBuilder();
        int tickets = rand.nextInt(5) + 1;
        ArrayList<String> flights = new ArrayList<String>();
        String flightNumber;
        for (int i = 0; i < tickets; i++) {
            flightNumber = setFlights.get(rand.nextInt(setFlights.size()));
            flights.add(flightNumber);
            stringBuilder.append(String.format(exampleTicket, getType(), getRandomString(3), getPrice(), flightNumber,
                    generateEmail(), generateName(), generateName(), generateName()));
        }
        stringBuilder.delete(stringBuilder.length() - 1, stringBuilder.length());
        customMap.put("data", String.format(exampleRow, generateEmail(), String.valueOf(stringBuilder)));
        customMap.put("flight_numbers", flights);
        return customMap;
    }

    private static String getRandomString(int k) {
        String charList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
        return generateWithList(k, charList);
    }

    private static String generateWithList(int k, String charList) {
        StringBuilder line = new StringBuilder();
        for (int i = 0; i < k; i++) {
            line.append(charList.charAt(rand.nextInt(charList.length())));
        }
        return String.valueOf(line);
    }

    private static String getPrice() {
        int maxValue = 1500;
        int minValue = 30;
        maxValue = maxValue - minValue;
        return String.format(Locale.US, "%.2f", (rand.nextDouble() * maxValue + minValue));
    }

    private static String getType() {
        String[] array = new String[]{"Low", "Medium", "High"};
        return array[rand.nextInt(array.length)];
    }

    private static String generateName() {
        String charList = "abcdefghijklmnopqrstuvwxyz";
        return generateWithList(rand.nextInt(30) + 10, charList);
    }

    private static String generateEmail() {
        String charList = "abcdefghijklmnopqrstuvwxyz1234567890";
        String[] tokens = new String[]{"hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com", "yandex.ru", "mail.ru"};
        return String.format("%s@%s", generateWithList(rand.nextInt(30) + 5, charList), tokens[rand.nextInt(tokens.length)]);
    }

    private static void fillCounterReservations(int n) {
        for (int i = 0; i < n; i++) {
            session.execute(String.format(updateCQL, 0, getRandomString(5)));
        }
    }

    public static void main(String[] args) {

//        fillCounterReservations(10);
        initFlights();
        String cqlStatement;
        HashMap<String, Object> maps;
        int n = args.length > 0 ? Integer.parseInt(args[0]) : 1;
        for (int i = 0; i < n; i++) {
            maps = generateData();
            cqlStatement = String.format(insertCQL, maps.get("data"));
            session.execute(cqlStatement);
            for (String flight : (ArrayList<String>) maps.get("flight_numbers")) {
                cqlStatement = String.format(updateCQL, 1, flight);
                session.execute(cqlStatement);
            }
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        cluster.close();
    }


}
