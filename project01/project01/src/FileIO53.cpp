/*
 * FileIO53.cpp
 *
 *  Created on: Jan 30, 2014
 *      Author: gregoryjeckell
 */

#include "FileIO53.h"

FileIO53::FileIO53(int& l, int& b, std::string diskName, int flag_empty)
{
	logical_blocks = l;
	block_size = b;
	diskID = diskName;
	ldisk = new char*[logical_blocks];
	for (int i=0; i < block_size; ++i) {
		ldisk[i] = new char[block_size];
		for (int j=0; j < block_size; ++j) {
			ldisk[i][j] = flag_empty;
		}
	}
}

FileIO53::~FileIO53()
{
	for (int i=0; i < logical_blocks; ++i) {
		delete ldisk[i];
	}
	delete [] ldisk;
}

void FileIO53::read_block(int i, char* p)
{
	for (int j=0; j < block_size; ++j) {
		p[j] = ldisk[i][j];
	}
}

void FileIO53::write_block(int i, const char* p)
{
	for (int j=0; j < block_size; ++j) {
		ldisk[i][j] = p[j];
	}
	ldisk[i][block_size] = '\0';
}

void FileIO53::saveDisk()
{
	std::ofstream outFile(diskID.c_str(), std::ios::out); //(diskID.c_str(), std::ios::out | std::ios::binary);
	if (outFile.is_open()) {
		for (int i=0; i < logical_blocks; ++i) {
			ldisk[i][block_size] = '\0';
			outFile << ldisk[i] << std::endl;
		}
	}
	outFile.close();
}

void FileIO53::restoreDisk()
{
	std::ifstream inFile(diskID.c_str());
	if (inFile.is_open()) {
		for (int i=0; i < logical_blocks; ++i) {
			inFile.getline(ldisk[i], block_size);
		}
	}
	inFile.close();
}

void FileIO53::restoreDisk(std::string diskName)
{
	std::ifstream inFile(diskName.c_str());
	if (inFile.is_open()) {
		for (int i=0; i < logical_blocks; ++i) {
			inFile.getline(ldisk[i], block_size);
		}
	} else {
		std::cout << "Disk " << diskName << " could not be opened" << std::endl;
	}
	inFile.close();
}

std::string FileIO53::toString()
{
	std::stringstream ss;
	for (int i=0; i < logical_blocks; ++i) {
		for (int j=0; j < block_size; ++j) {
			ss << ldisk[i][j];
		}
		ss << '\n';
	}
	return ss.str();
}
