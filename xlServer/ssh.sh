#!/usr/bin/env expect
set password 654321
set name root
foreach HOST { zkyserver zkymaster zky5 zky6 zky7 zky11 zky12 zky13 zky14 zky15 zky16 zky17 zky18 zky19 zky20 zky21 zky22 zky30 zky31 zky32 zky40 zky41 zky42 zky50 zky51 zky52 zky60 zky61 zky62 zky70 zky71 zky72 zky80 zky81 zky82 } { 
    spawn ssh $HOST -l $name
    expect {
      "(yes/no)" {
            send "yes\n"
            expect "*password:" { send "$password\n" }
      }
    }
    expect "*password:" { send "$password\n" }
    expect "*#" { send "su hadoop\n" }
    expect "*" { send "mkdir /home/hadoop/hbase.bk.12-11-7\n" }
    expect "*" { send "cp -ar /home/hadoop/hbase-0.92.1/logs /home/hadoop/hbase.bk.12-11-7\n" }
    expect "*" { send "cp -ar /home/hadoop/hbase-0.92.1/tmp /home/hadoop/hbase.bk.12-11-7\n" }
    expect eof
}
