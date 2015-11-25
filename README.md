#Ambari Config Audit

This python script generates a config audit log file. This file basically contains the configs changes between different Ambari-managed Hadoop configurations (e.g. hdfs-site, hive-site,...)

#Usage

General Syntax:
```
python audit.py --target <host+port> --cluster <clustername> --user <ambari_username> --output <filename> --https [True|False] --config <config-name>
```

Example (audit hive-site to shell):
```
python audit.py --target horton01.myhost.com:8080 --cluster bigdata --user admin --config hive-site
```

Example (audit hive-site to hive-site_audit.log)
```
python audit.py --target horton01.myhost.com:8080 --cluster bigdata --user admin --config hive-site --output hive-site_audit.log
```

#Result (example, hive-site)
Example result for `hive-site`

```
ive-site: version 1 - ADDED - javax.jdo.option.ConnectionDriverName - com.mysql.jdbc.Driver
hive-site: version 1 - ADDED - hive.fetch.task.aggr - false
hive-site: version 1 - ADDED - hive.execution.engine - tez
hive-site: version 1 - ADDED - hive.tez.java.opts - -server -Djava.net.preferIPv4Stack=true -XX:NewRatio=8 -XX:+UseNUMA -XX:+UseG1GC -XX:+ResizeTLAB -XX:+PrintGCDetails -verbose:gc -XX:+PrintGCTimeStamps
hive-site: version 1 - ADDED - hive.vectorized.groupby.maxentries - 100000
hive-site: version 1 - ADDED - hive.server2.table.type.mapping - CLASSIC
...
...
...
hive-site: version 1 - ADDED - hive.compactor.check.interval - 300L
hive-site: version 1 - ADDED - hive.compactor.delta.pct.threshold - 0.1f
hive-site: version 2 - CHANGED - javax.jdo.option.ConnectionURL - jdbc:mysql://horton03.myhost.com/hive?createDatabaseIfNotExist=true => jdbc:mysql://horton03.myhost.com:3306/hive?createDatabaseIfNotExist=true
hive-site: version 2 - CHANGED - hive.zookeeper.quorum - horton03.myhost.com:2181,horton02.myhost.com:2181,horton01.myhost.com:2181 => horton02.myhost.com:2181,horton03.myhost.com:2181,horton01.myhost.com:2181
hive-site: version 2 - CHANGED - hive.cluster.delegation.token.store.zookeeper.connectString - horton03.myhost.com:2181,horton02.myhost.com:2181,horton01.myhost.com:2181 => horton02.myhost.com:2181,horton03.myhost.com:2181,horton01.myhost.com:2181
hive-site: version 3 - CHANGED - javax.jdo.option.ConnectionURL - jdbc:mysql://horton03.myhost.com:3306/hive?createDatabaseIfNotExist=true => jdbc:mysql://horton03.myhost.com/hive?createDatabaseIfNotExist=true
hive-site: version 4 - ADDED - atlas.cluster.name - default
hive-site: version 4 - CHANGED - hive.exec.post.hooks - org.apache.hadoop.hive.ql.hooks.ATSHook => org.apache.hadoop.hive.ql.hooks.ATSHook,org.apache.atlas.hive.hook.HiveHook
hive-site: version 4 - CHANGED - hive.metastore.sasl.enabled - false => true
hive-site: version 4 - CHANGED - hive.server2.authentication.spnego.principal - /etc/security/keytabs/spnego.service.keytab => HTTP/_HOST@EXAMPLE.COM
hive-site: version 4 - CHANGED - hive.server2.authentication.spnego.keytab - HTTP/_HOST@EXAMPLE.COM => /etc/security/keytabs/spnego.service.keytab
hive-site: version 4 - ADDED - hive.server2.authentication.kerberos.keytab - /etc/security/keytabs/hive.service.keytab
hive-site: version 4 - CHANGED - hive.zookeeper.quorum - horton02.myhost.com:2181,horton03.myhost.com:2181,horton01.myhost.com:2181 => horton03.myhost.com:2181,horton02.myhost.com:2181,horton01.myhost.com:2181
hive-site: version 4 - ADDED - hive.server2.authentication.kerberos.principal - hive/_HOST@EXAMPLE.COM
hive-site: version 4 - ADDED - atlas.rest.address - http://horton03.myhost.com:21000
hive-site: version 4 - CHANGED - hive.cluster.delegation.token.store.zookeeper.connectString - horton02.myhost.com:2181,horton03.myhost.com:2181,horton01.myhost.com:2181 => horton03.myhost.com:2181,horton02.myhost.com:2181,horton01.myhost.com:2181
hive-site: version 4 - CHANGED - hive.server2.authentication - NONE => KERBEROS
hive-site: version 5 - CHANGED - atlas.cluster.name - default => bigdata
hive-site: version 6 - ADDED - my.prop.test - blub
```
