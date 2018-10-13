package com.delta;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Session;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;
import java.util.Random;

public class App {

    final static private Random rand = new Random();

    private static HashMap<String, Object> generateData() {
        HashMap<String, Object> customMap = new HashMap<String, Object>();
        String exampleRow = "('%s', toTimeStamp(now()), [%s])";
        String exampleTicket = "{type:'%s', place:'%s', price:%s, flight_number:'%s', passport_data:{email:'%s', first_name:'%s', last_name:'%s', third_name:'%s'}},";
        StringBuilder stringBuilder = new StringBuilder();
        int tickets = rand.nextInt(5);
        ArrayList<String> flights = new ArrayList<String>();
        String flightNumber;
        for (int i = 0; i < tickets; i++) {
            flightNumber = getRandomString(5);
            flights.add(flightNumber);
            stringBuilder.append(String.format(exampleTicket, getType(), getRandomString(3), getPrice(), flightNumber,
                     generateEmail(), generateName(), generateName(), generateName()));
        }
        System.out.println(stringBuilder.charAt(stringBuilder.length() - 1));
        stringBuilder.delete(stringBuilder.length() - 1, stringBuilder.length());
        System.out.println(stringBuilder);
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
        String[] tokens= new String[]{"hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com", "yandex.ru", "mail.ru"};
        return String.format("%s@%s", generateWithList(rand.nextInt(30)+ 5, charList), tokens[rand.nextInt(tokens.length)]);
    }

    public static void main(String[] args) {
        final String serverIp = "127.0.0.1";
        final String keyspace = "avia";
        final String insertCQL = "INSERT INTO reservation (passenger, date, tickets) VALUES %s";
        final String updateCQL = "UPDATE counter_reservations SET amount_reservations = amount_reservations + 1 WHERE flight_number = '%s'";

        Cluster cluster = Cluster.builder()
                .addContactPoints(serverIp)
                .build();
        Session session = cluster.connect(keyspace);
        String cqlStatement;
        HashMap<String, Object> maps;
        int n = args.length > 0 ? Integer.parseInt(args[0]) : 1;
        for (int i = 0; i < n; i++) {
            maps = generateData();
            cqlStatement = String.format(insertCQL, maps.get("data"));
            session.execute(cqlStatement);
            for (String flight : (ArrayList<String>) maps.get("flight_numbers")) {
                cqlStatement = String.format(updateCQL, flight);
                session.execute(cqlStatement);
            }
        }
        cluster.close();
    }


}
