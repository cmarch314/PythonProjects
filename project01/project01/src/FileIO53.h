/*
 * FileIO53.h
 *
 *  Created on: Jan 30, 2014
 *      Author: gregoryjeckell
 */

#ifndef FILEIO53_H_
#define FILEIO53_H_
#include <iostream>
#include <fstream>
#include <sstream>

class FileIO53 {
public:
	FileIO53(int& l, int& b, std::string diskName, int flag_empty);
	~FileIO53();
	void read_block(int i, char* p);
	void write_block(int i, const char* p);

	void saveDisk();
	void restoreDisk();
	void restoreDisk(std::string diskName);
	std::string toString();

private:
	char** ldisk;
	std::string diskID;
	int logical_blocks;
	int block_size;
};

#endif /* FILEIO53_H_ */
