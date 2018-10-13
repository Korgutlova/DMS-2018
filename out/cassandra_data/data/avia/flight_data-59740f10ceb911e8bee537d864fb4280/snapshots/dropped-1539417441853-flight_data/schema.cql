CREATE TABLE IF NOT EXISTS avia.flight_data (
	flight_number text,
	plane_identificator text,
	speed int,
	engine_condition text,
	weather_condition text,
	temperature_overboard int,
	distance_passed counter,
	PRIMARY KEY ((flight_number, plane_identificator), speed, engine_condition, weather_condition, temperature_overboard))
	WITH ID = 59740f10-ceb9-11e8-bee5-37d864fb4280
	AND CLUSTERING ORDER BY (speed ASC, engine_condition ASC, weather_condition ASC, temperature_overboard ASC)
	AND bloom_filter_fp_chance = 0.01
	AND dclocal_read_repair_chance = 0.1
	AND crc_check_chance = 1.0
	AND default_time_to_live = 0
	AND gc_grace_seconds = 864000
	AND min_index_interval = 128
	AND max_index_interval = 2048
	AND memtable_flush_period_in_ms = 0
	AND read_repair_chance = 0.0
	AND speculative_retry = '99PERCENTILE'
	AND comment = ''
	AND caching = { 'keys': 'ALL', 'rows_per_partition': 'NONE' }
	AND compaction = { 'max_threshold': '32', 'min_threshold': '4', 'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy' }
	AND compression = { 'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor' }
	AND cdc = false
	AND extensions = {  };
