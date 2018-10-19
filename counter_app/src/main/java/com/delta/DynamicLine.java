package com.delta;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.Timer;
import javax.swing.JPanel;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Session;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.time.Millisecond;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.time.TimeSeriesCollection;
import org.jfree.data.xy.XYDataset;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;

public class DynamicLine extends ApplicationFrame implements ActionListener {

    private TimeSeries series;
    private long lastValue;
    private String selectCQL = "SELECT amount_reservations FROM counter_reservations WHERE flight_number='%s'";
    static private Session session;

    static {
        String serverIp = "127.0.0.1";
        String keyspace = "avia";
        Cluster cluster = Cluster.builder()
                .addContactPoints(serverIp)
                .build();
        session = cluster.connect(keyspace);
    }

    private long getValueCounter() {
        ResultSet rs = session.execute(selectCQL);
        return rs.one().getLong("amount_reservations");
    }

    public DynamicLine(final String title, String flight) {

        super(title);
        this.series = new TimeSeries("Counter", Millisecond.class);
        selectCQL = String.format(selectCQL, flight);
        this.lastValue = getValueCounter();
        final TimeSeriesCollection dataset = new TimeSeriesCollection(this.series);
        final JFreeChart chart = createChart(dataset);

        /**
         * Timer to refresh graph after every 1/4th of a second
         */
        Timer timer = new Timer(250, this);
        timer.setInitialDelay(1000);

        //Sets background color of chart
        chart.setBackgroundPaint(new Color(0x949FFF));

        //Created JPanel to show graph on screen
        final JPanel content = new JPanel(new BorderLayout());

        //Created Chartpanel for chart area
        final ChartPanel chartPanel = new ChartPanel(chart);

        //Added chartpanel to main panel
        content.add(chartPanel);

        //Sets the size of whole window (JPanel)
        chartPanel.setPreferredSize(new java.awt.Dimension(900, 600));

        //Puts the whole content on a Frame
        setContentPane(content);

        timer.start();

    }

    private JFreeChart createChart(final XYDataset dataset) {
        final JFreeChart result = ChartFactory.createTimeSeriesChart(
                super.getTitle(),
                "Time",
                "Tickets counter",
                dataset,
                true,
                true,
                false
        );

        final XYPlot plot = result.getXYPlot();

        plot.setBackgroundPaint(new Color(0xffffe0));
        plot.setDomainGridlinesVisible(true);
        plot.setDomainGridlinePaint(Color.lightGray);
        plot.setRangeGridlinesVisible(true);
        plot.setRangeGridlinePaint(Color.lightGray);

        ValueAxis xaxis = plot.getDomainAxis();
        xaxis.setAutoRange(true);

        //Domain axis would show data of 60 seconds for a time
        xaxis.setFixedAutoRange(60000.0);  // 60 seconds
        xaxis.setVerticalTickLabels(true);

        ValueAxis yaxis = plot.getRangeAxis();
        yaxis.setRange(0.0, 1000);
        yaxis.setAutoRange(true);

        return result;
    }

    public void actionPerformed(final ActionEvent e) {

        this.lastValue = getValueCounter();

        final Millisecond now = new Millisecond();
        this.series.add(new Millisecond(), this.lastValue);

        System.out.println("Current Time in Milliseconds = " + now.toString() + ", Current Value : " + this.lastValue);
    }

    public static void main(final String[] args) {

        String flight = args.length > 0 ? args[0] : "CTAHE";
        final DynamicLine demo = new DynamicLine(String.format("Purchased tickets for flights '%s'", flight), flight);
        demo.pack();
        RefineryUtilities.centerFrameOnScreen(demo);
        demo.setVisible(true);

    }

}