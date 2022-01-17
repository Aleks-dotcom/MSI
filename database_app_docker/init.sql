USE igralci
CREATE TABLE igralci.data(
	id int(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	proga INT(6),
	score VARCHAR(10),
	scoreNumeric DOUBLE
)
