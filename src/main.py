import common

x = common.get_db_hander('cdn_mat')
sql = "select * from cdn_test"
y = x.query(sql)
print(y)
info_logger = common.get_logger("info")
error_logger = common.get_logger("error")
info_logger.info("abfsljflksd")
error_logger.error("sfj;sjfklslkfsd")