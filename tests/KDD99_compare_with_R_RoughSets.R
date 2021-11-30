
library(sets)
library(RoughSets)

columns = c("duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_hot_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","target")


source("https://raw.githubusercontent.com/darekjk/R/master/DJ.RoughSets.functions.R")
source("https://raw.githubusercontent.com/janusza/RoughSets/master/R/IOFunctions.R")   # import funkcji niedostepnych z poziomu biblioteki RoughSets, m.in. ObjectFactory
source("https://raw.githubusercontent.com/darekjk/R/master/LEM2.R")

# see:
# https://peerj.com/preprints/1954.pdf
# http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html

# classes: back,buffer_overflow,ftp_write,guess_passwd,imap,ipsweep,land,loadmodule,multihop,neptune,nmap,normal,perl,phf,pod,portsweep,rootkit,satan,smurf,spy,teardrop,warezclient,warezmaster.

filename = "D:\\git\\AI\\KDD99_DATA\\kddcup.data.corrected.gz"

## locale-specific version of date()
format(Sys.time(), "%a %b %d %X %Y")

system.time({
  df <- read.csv(file = filename, header = FALSE, fileEncoding = "UTF-8", sep=",")
})
#  user  system elapsed 
# 249.33    6.05  302.97 
# user  system elapsed 
# 259.25   16.46  485.55 

A = c(1:41)
AD = c(1:42)
dec_attr = 42

system.time({
  DT = RoughSets::SF.asDecisionTable(df, decision.attr = dec_attr, indx.nominal = AD)
})
#    user  system elapsed 
# 143.47    5.40  177.52 



system.time({
  IND.A <- BC.IND.relation.RST(DT, A)
  LU.A = BC.LU.approximation.RST(DT, IND.A)
})
#    user  system elapsed 
# 492.27   positive.reg 8.75  539.34 
#user  system elapsed 
#342.07    7.55  387.06 


system.time({
  POS.A = BC.positive.reg.RST(decision.table = DT, roughset = LU.A)
  #POS.A$positive.reg
  
  boundary = BC.boundary.reg.RST(decision.table = DT, roughset = LU.A)
  #boundary$boundary.reg

  NEG.A = BC.negative.reg.RST(decision.table = DT, roughset = LU.A)
  #NEG.A$negative.reg
})

#  user  system elapsed 
# 36.02    0.88   41.43 

# Save vector as .csv
system.time({
  df.tmp = data.frame(objects=POS.A$positive.reg-1)
  write.csv(df.tmp, "kdd_positive_region_A.csv", row.names = FALSE, quote=FALSE )
  
  df.tmp = data.frame(objects=boundary$boundary.reg-1)
  write.csv(df.tmp, "kdd_boundary_region_A.csv", row.names = FALSE, quote=FALSE )
  
  df.tmp = data.frame(objects=NEG.A$negative.reg-1)
  write.csv(df.tmp, "kdd_negative_region_A.csv", row.names = FALSE, quote=FALSE )
  
 })
# user  system elapsed 
# 27.20    9.83   68.72 

# elapsed is the wall clock time taken to execute the function
# As for user and system times, William Dunlap has posted a great explanation to the r-help mailing list:

## locale-specific version of date()
format(Sys.time(), "%a %b %d %X %Y")

# Totql: 16 min 12 sek




B = c(1:2)

system.time({
  DT = RoughSets::SF.asDecisionTable(df, decision.attr = dec_attr, indx.nominal = AD)
})
#    user  system elapsed 
# 143.47    5.40  177.52 



system.time({
  IND.B <- BC.IND.relation.RST(DT, B)
  LU.B = BC.LU.approximation.RST(DT, IND.B)
})
#    user  system elapsed 
# 492.27   positive.reg 8.75  539.34 
#user  system elapsed 
#342.07    7.55  387.06 


system.time({
  POS.B = BC.positive.reg.RST(decision.table = DT, roughset = LU.B)
  #POS.A$positive.reg
  
  boundary.B = BC.boundary.reg.RST(decision.table = DT, roughset = LU.B)
  #boundary$boundary.reg
  
  NEG.B = BC.negative.reg.RST(decision.table = DT, roughset = LU.B)
  #NEG.A$negative.reg
})

#  user  system elapsed 
# 36.02    0.88   41.43 

# Save vector as .csv
system.time({
  df.tmp = data.frame(objects=POS.B$positive.reg-1)
  write.csv(df.tmp, "kdd_positive_region_B.csv", row.names = FALSE, quote=FALSE )
  
  df.tmp = data.frame(objects=boundary$boundary.B.reg-1)
  write.csv(df.tmp, "kdd_boundary_region_B.csv", row.names = FALSE, quote=FALSE )
  
  df.tmp = data.frame(objects=NEG.B$negative.reg-1)
  write.csv(df.tmp, "kdd_negative_region_B.csv", row.names = FALSE, quote=FALSE )})
# user  system elapsed 
# 27.20    9.83   68.72 







“User CPU time” gives the CPU time spent by the current process 
(i.e., the current R session) and “system CPU time” gives the CPU time 
spent by the kernel (the operating system) on behalf of the current process. 

The operating system is used for things like opening files, 
doing input or output, starting other processes, and looking at the system clock: 
  operations that involve resources that many processes must share. 

Different operating systems will have different things done by the operating system.

More benchmark methds:
  https://www.r-bloggers.com/2017/05/5-ways-to-measure-running-time-of-r-code/
  
  
