//============================================================================
// Name        : FileSystem53.cpp
// Author      :
// Version     :
// Copyright   : Your copyright notice
// Description : First Project Lab
//============================================================================

#include <iostream>
#include <string>
#include <cstring>
#include <stdlib.h>
#include <stdio.h>
#include "FileIO53.h"
using namespace std;

#define DEBUG 1

class FileSystem53
{
    public:

	/* Constructor of this File system.
		 *   1. Initialize IO system.
		 *   2. Format it if not done.
		 */
	FileSystem53(int l, int b, string diskName) {
		sys_io = new FileIO53(l, b, diskName, FLAG_EMPTY);
		desc_table = new char*[l];
		for (int i=0; i < l; ++i) {
			desc_table[i] = new char[b];
		}
		OpenFileTable();
		format();
		save();
	}

	// Open File Table(OFT).
	void OpenFileTable()
	{
		oft = new char*[BLOCK_SIZE];
		for (int i=0; i < OFT_ROWS; ++i) {
			oft[i] = new char[OFT_COLS];
		}
	}

	// Allocate open file table
	int find_oft()
	{
		for (int i=1; i < OFT_ROWS; ++i) {
			if (oft[i][OFT_OPEN_FLAG_INDEX] == 0) {
				return i;
			}
		}
		return FLAG_ERROR_FULL; // Handle error
	}

	//Deallocate
	void deallocate_oft(int index)
	{
		for (int i=0; i < OFT_ROWS; ++i) {
			delete oft[i];
		}
		delete [] oft;
	}

	/* Format file system.
	 *   1. Initialize the first K blocks with zeros.
	 *   2. Create root directory descriptor for directory file.
	 * Parameter(s):
	 *   none
	 * Return:
	 *   none
	 */
	void format()
	{
		// initialize desc_table
		for (int i=0; i < K; ++i) {
			for (int j=0; j < MAX_BLOCK_NO; ++j) {
				desc_table[i][j] = FLAG_EMPTY;
			}
		}

		// initialize bitmap
		for (int i=0; i < 7; ++i) {
			desc_table[0][i] = '1';
		}

		// create directory file
		char directory[BLOCK_SIZE];
		for (int i=0; i < BLOCK_SIZE; ++i) {
			directory[i] = FLAG_EMPTY;
		}

		// write directory to disk
		write_descriptor(0, directory);
		int emptyBlockIndex = find_empty_block();
		desc_table[0][emptyBlockIndex] = '1';
		sys_io->write_block(emptyBlockIndex, directory); // here we initialize the first block of the dir
		oft[0][OFT_CURR_POS_INDEX] = 0;
		oft[0][OFT_CURR_BLOCK] = emptyBlockIndex;
		oft[0][OFT_FILE_SIZE] = 0;
		update_desc_block(0, 0, emptyBlockIndex);
		update_desc_size(0, 0);
	}


	/* Read descriptor
	 * Parameter(s):
	 *    no: Descriptor number to read
	 * Return:
	 *    Return char[16] of descriptor
	 */
	char* read_descriptor(int no)
	{
		char* descriptor = new char[16]; // call to new. Must release memory at caller.
		int row = (no / 4) + 1;
		int col = (no % 4) * 16;
		for (int i=0; i < 16; ++i) {
			descriptor[i] = desc_table[row][col++];
		}
		return descriptor;
	}

	/* Clear descriptor
	 *   1. Clear descriptor entry
	 *   2. Clear bitmap
	 *   3. Write back to disk
	 * Parameter(s):
	 *    no: Descriptor number to clear
	 * Return:
	 *    none
	 */
	void clear_descriptor(int no)
	{
		int row = (no / 4) + 1;
		int col = (no % 4) * 16;

		for (int i=0; i < 16; ++i) {
			desc_table[row][col++] = FLAG_EMPTY;
		}
	}

	void clear_oft_buffer(int index)
	{
		for (int i=0; i < BLOCK_SIZE; ++i) {
			oft[index][i] = FLAG_EMPTY;
		}
	}

	/* Write descriptor
	 *   1. Update descriptor entry
	 *   2. Mark bitmap
	 *   3. Write back to disk
	 * Parameter(s):
	 *    no: Descriptor number to write
	 *    desc: descriptor to write
	 * Return:
	 *    none
	 */
	void write_descriptor(int no, char* desc)
	{
		// get row and column of desc_table
		int row = (no / 4) + 1;
		int col = (no % 4) * 16;

		for (int i=0; i < 16; ++i) {
			desc_table[row][col++] = desc[i];
		}
	}

	void update_desc_size(int descNum, int value)
	{
		char v[4];
		numberToCharArray(value, v, 4);

		// get row and column of desc_table
		int row = (descNum / 4) + 1;
		int col = (descNum % 4) * 16;
		for (int i=0; i < 4; ++i) {
			desc_table[row][col++] = v[i];
		}
	}

	void update_desc_block(int descNum, int blockNum, int value)
	{
		// get row and column of desc_table
		int row = (descNum / 4) + 1;
		int col = (descNum % 4) * 16;

		char v[4];
		numberToCharArray(value, v, 4);
		switch(blockNum) {
		case 0:
			col += 4;
			break;
		case 1:
			col += 8;
			break;
		case 2:
			col += 12;
			break;
		}

		for (int i=0; i < 4; ++i) {
			desc_table[row][col++] = v[i];
		}

		if (DEBUG) {
			cout << "Updated DescNum " << descNum << " at block " << blockNum << " with value " << value << endl;
		}
	}

	int get_desc_block_value(int descNum, int blockNum)
	{
		// get row and column of desc_table
		int row = (descNum / 4) + 1;
		int col = (descNum % 4) * 16;

		char v[4];
		switch(blockNum) {
		case 0:
			col += 4;
			break;
		case 1:
			col += 8;
			break;
		case 2:
			col += 12;
			break;
		}
		for (int i=0; i < 4; ++i) {
			v[i] = desc_table[row][col++];
		}
		return charArrayToNumber<int>(v);
	}

	int get_desc_size(int descNum)
	{
		// get row and column of desc_table
		int row = (descNum / 4) + 1;
		int col = (descNum % 4) * 16;

		char v[4];

		for (int i=0; i < 4; ++i) {
			v[i] = desc_table[row][col++];
		}
		return charArrayToNumber<int>(v);
	}

	/* Search for an unoccupied descriptor.
	 * If ARRAY[0] is zero, this descriptor is not occupied.
	 * Then it returns descriptor number.
	 */
	int find_empty_descriptor()
	{
		for (int i=1; i < MAX_FILE_NO; ++i) { // start at 1 to avoid directory file
			int row = (i / 4) + 1;
			int col = (i % 4) * 16;
			if (desc_table[row][col] == FLAG_EMPTY) {
				return i;
			}
		}
		return FLAG_ERROR_FULL;
	}


	/* Search for an unoccupied block.
	 *   This returns the first unoccupied block in bitmap field.
	 *   Return value -1 means all blocks are occupied.
	 * Parameter(s):
	 *    none
	 * Return:
	 *    Returns the block number
	 *    -1 if not found
	 */
	int find_empty_block()
	{
		for (int i=K; i < MAX_BLOCK_NO; ++i) {
			if (desc_table[0][i] == FLAG_EMPTY) {
				return i;
			}
		}
		return FLAG_ERROR_FULL;
	}


	/* Get one character.
	 *    Returns the character currently pointed by the internal file position
	 *    indicator of the specified stream. The internal file position indicator
	 *    is then advanced to the next character.
	 * Parameter(s):
	 *    index (descriptor number of the file to be added.)
	 * Return:
	 *    On success, the character is returned.
	 *    If a writing error occurs, EOF is returned.
	 */
	char fgetc(int index)
	{
		int curr = oft[index][OFT_CURR_POS_INDEX];
		if (curr > 63)
			return FLAG_ERROR_EOF;
		oft[index][OFT_CURR_POS_INDEX] = curr + 1;
		return oft[index][curr];
	}


	/* Put one character.
	 *    Writes a character to the stream and advances the position indicator.
	 *    The character is written at the position indicated by the internal position
	 *    indicator of the file, which is then automatically advanced by one.
	 * Parameter(s):
	 *    c: character to write
	 *    index (descriptor number of the file to be added.)
	 * Return:
	 *    On success, the character written is returned.
	 *    If a writing error occurs, -2 is returned.
	 */
	char fputc(char c, int index)
	{
		int curr = oft[index][OFT_CURR_POS_INDEX];

		if (curr > 63) {
			cout << "Error: " << FLAG_ERROR_EOF << "EOF" << endl;
			return FLAG_ERROR_EOF;
		}

		oft[index][curr] = c;

		if (DEBUG) {
			cout << "Placed char :" << c << " at index: " << index << " in position: " << curr << endl;
			cout << "OFT[index]: " << oft[index] << endl;
		}

		oft[index][OFT_CURR_POS_INDEX] = curr + 1;
		oft[index][OFT_FILE_SIZE] += 1;
		update_desc_size(oft[index][OFT_FILE_DESC_INDEX], oft[index][OFT_FILE_SIZE]);
		return oft[index][curr];
	}


	/* Check for the end of file.
	 * Parameter(s):
	 *    index (descriptor number of the file to be added.)
	 * Return:
	 *    Return true if end-of-file reached.
	 */
	bool feof(int index)
	{

	}


	/* Search for a file
	 * Parameter(s):
	 *    index: index of open file table
	 *    st: The name of file to search.
	 * Return:
	 *    index: An integer number position of found file entry.
	 *    Return -1 if not found.
	 */
	int search_dir(int index, string symbolic_file_name)
	{
		char name[4];
		for (int i=0; i < 4; ++i) {
			name[i] = symbolic_file_name[i];
		}

		int curr_block = get_desc_block_value(0, index);
		if (curr_block != 0) {
			char* b = new char[64];
			sys_io->read_block(curr_block, b);
			for (int j=0; j < BLOCK_SIZE; j += 8) {
				int found_count = 0;
				for (int k=0; k < 4; ++k) {
					if (name[k] == b[j+k]) {
						if (DEBUG) {
							cout << "Found match k: " << name[k] << " b: " << b[j+k] << endl;
						}
						++found_count;
					}
				}
				if (found_count >= 4)
					return j;
			}
		}

		return FLAG_ERROR_NOTFOUND;
	}


	/* Clear a file entry from directory file
	 *
	 * Parameter(s):
	 *    index: open file table index
	 *    start_pos:
	 *    length:
	 * Return:
	 *    none
	 */
	void delete_dir(int index, int start_pos, int len)
	{

	}


	/* File creation function:
	 *    1. creates empty file with file size zero.
	 *    2. makes/allocates descriptor.
	 *    3. updates directory file.
	 * Parameter(s):
	 *    symbolic_file_name: The name of file to create.
	 * Return:
	 *    Return 0 for successful creation.
	 *    Return -1 for error (no space in disk)
	 *    Return -2 for error (for duplication)
	 */
	int create(string symbolic_file_name)
	{
		int desc_index = find_empty_descriptor();
		if (desc_index == FLAG_ERROR_FULL) {
			cout << "Error: no empty descriptors left";
			return FLAG_ERROR_FULL;
		}
		char descriptor[16] = {'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'};
		write_descriptor(desc_index, descriptor);

		// Search for duplicates
		bool found = false;
		int directory_block = FLAG_ERROR_NOTFOUND;
		for (int i=0; i < 3; ++i) { // for each directory block

			int check_pos = search_dir(i, symbolic_file_name);
			if (check_pos != FLAG_ERROR_NOTFOUND) {
				return FLAG_ERROR_FILEEXISTS;
			}

			// Find empty entry
			directory_block = get_desc_block_value(0, i);
			if (directory_block != 0) {
				sys_io->read_block(directory_block, oft[0]);
				oft[0][OFT_CURR_BLOCK] = directory_block;
				for (int j=0; j < BLOCK_SIZE && !found; ++j) {
					if (oft[0][j] == FLAG_EMPTY) {
						if (DEBUG) {
							cout << "i: " << i << " Block # " << directory_block << endl;
							cout << "looking at: " << oft[0][j] << endl;
							cout << "FOUND IT! at j; " << j << endl;
						}
						found = true;
						oft[0][OFT_CURR_POS_INDEX] = j;
					}
				}
			}
		}

		// If directory file grows too large, get new block
		if ((oft[0][OFT_CURR_POS_INDEX] > 63) && (oft[0][OFT_FILE_SIZE] < (BLOCK_SIZE*3))) {
			int newBlock;
			newBlock = find_empty_block();
			desc_table[0][newBlock] = '1';
			clear_oft_buffer(0);
			oft[0][OFT_CURR_BLOCK] = newBlock;
			oft[0][OFT_CURR_POS_INDEX] = 0;
			oft[0][OFT_FILE_DESC_INDEX] = 0;
			update_desc_block(0, (int)(oft[0][OFT_FILE_SIZE]%BLOCK_SIZE)+1, newBlock);
		}

		// write file name name to oft
		for (unsigned int i=0; i < 4; ++i) {
			if (i > symbolic_file_name.length()-1) { // Make sure we write 4 chars
				fputc(' ', 0);
			} else {
				fputc(symbolic_file_name.c_str()[i], 0);
			}
		}

		// write descritor index to oft
		char desc_index_char[4];
		numberToCharArray(desc_index, desc_index_char, 4);
		for (int i=0; i < 4; ++i) {
			fputc(desc_index_char[i], 0);
		}

		update_desc_size(0, oft[0][OFT_FILE_SIZE]);
		sys_io->write_block(oft[0][OFT_CURR_BLOCK], oft[0]);
		save();

		if (DEBUG) {
			cout << "Wrote to disk at block num: "<< (int)oft[0][OFT_CURR_BLOCK] << endl;
			cout << sys_io->toString() << endl;
		}
	}


	/* Open file with descriptor number function:
	 * Parameter(s):
	 *    desc_no: descriptor number
	 * Return:
	 *    index: index if open file table if successfully allocated.
	 *    Return -1 for error.
	 */
	int open_desc(int desc_no)
	{
		int row = (desc_no / 4) + 1;
		int col = (desc_no % 4) * 16;
		if(oft) {
			int new_oft_index = find_oft();
			clear_oft_buffer(new_oft_index);
			oft[new_oft_index][OFT_FILE_SIZE] = get_desc_size(desc_no);
			oft[new_oft_index][OFT_CURR_POS_INDEX] = 0;
		}
	}


	/* Open file with file name function:
	 * Parameter(s):
	 *    symbolic_file_name: The name of file to open.
	 * Return:
	 *    index: An integer number, which is a index number of open file table.
	 *    Return -1 or -2 if it cannot be open.
	 */
	// TODOs:
			// 1. Open directory file
			// 2. Search for a file with given name
			//    Return -1 if not found.
			// 3. Get descriptor number of the found file
			// 4. Looking for unoccupied entry in open file table.
			//    Return -2 if all entry are occupied.
			// 5. Initialize the entry (descriptor number, current position, etc.)
			// 6. Return entry number
	int open(string symbolic_file_name)
	{
		int oft_index = find_oft();
		if (oft_index == FLAG_ERROR_FULL)
			return FLAG_ERROR_FULL;

		clear_oft_buffer(oft_index);
		int file_pos = FLAG_ERROR_NOTFOUND;
		bool found = false;
		for (int i=0; i < 3 && !found; ++i) { // for each directory block
			file_pos = search_dir(i, symbolic_file_name);
			if (file_pos != FLAG_ERROR_NOTFOUND) {
				found = true;
			}
		}

		// get descriptor number of found file
		char desc_num[4];
		int file_inc = file_pos+4;
		for (int i=0; i < 4; ++i) {
			desc_num[i] = oft[0][file_inc++];
		}
		int desc_number = charArrayToNumber<int>(desc_num);

		oft[oft_index][OFT_CURR_POS_INDEX] = 0;
		oft[oft_index][OFT_OPEN_FLAG_INDEX] = 1;
		oft[oft_index][OFT_FILE_DESC_INDEX] = desc_number;
		oft[oft_index][OFT_FILE_SIZE] = get_desc_size(desc_number);

		int curr_block = FLAG_EMPTY;
		for (int i=0; i < 3; ++i) {
			if (get_desc_block_value(desc_number, i) > 0) {
				curr_block = i;
			}
		}
		oft[oft_index][OFT_CURR_BLOCK] = curr_block;

		if (DEBUG)
			cout << "Opening to oft index: " << oft_index << endl;
		return oft_index;

	}


	/* File Read function:
	 *    This reads a number of bytes from the the file indicated by index.
	 *    Reading should start from the point pointed by current position of the file.
	 *    Current position should be updated accordingly after read.
	 * Parameter(s):
	 *    index: File index which indicates the file to be read.
	 *    mem_area: buffer to be returned
	 *    count: number of byte(s) to read
	 * Return:
	 *    Actual number of bytes returned in mem_area[].
	 *    -1 value for error case "File hasn't been open"
	 *    -2 value for error case "End-of-file"
	 TODOs:
			 1. Read the open file table using index.
			    1.1 Get the file descriptor number and the current position.
			    1.2 Can't get proper file descriptor, return -1.
			 2. Read the file descriptor
			    2.1 Get file size and block array.
			 3. Read 'count' byte(s) from file and store in mem_area[].
			    3.1 If current position crosses block boundary, call read_block() to read the next block.
			    3.2 If current position==file size, stop reading and return.
			    3.3 If this is called when current position==file size, return -2.
			    3.4 If count > mem_area size, only size of mem_area should be read.
			    3.5 Returns actual number of bytes read from file.
			    3.6 Update current position so that next read() can be done from the first byte haven't-been-read.
    */
	int read(int index, int count)
	{
		if (oft[index][OFT_OPEN_FLAG_INDEX] == 0)
			return FLAG_ERROR_NOTFOUND;

		int bytes_read = 0;
		for (int i=0; i < count; ++i) {
			cout << fgetc(index);
			bytes_read++;
		}
		return bytes_read;
	}


	/* File Write function:
	 *    This writes 'count' number of 'value'(s) to the file indicated by index.
	 *    Writing should start from the point pointed by current position of the file.
	 *    Current position should be updated accordingly.
	 * Parameter(s):
	 *    index: File index which indicates the file to be read.
	 *    value: a character to be written.
	 *    count: Number of repetition.
	 * Return:
	 *    >0 for successful write
	 *    -1 value for error case "File hasn't been open"
	 *    -2 for error case "Maximum file size reached" (not implemented.)
	 */
	int write(int index, char value, int count)
	{
		if (oft[index][OFT_OPEN_FLAG_INDEX] == 0)
			return FLAG_ERROR_NOTFOUND;

		if (oft[index][OFT_CURR_BLOCK] == FLAG_EMPTY) {
			int newBlock = find_empty_block();
			oft[index][OFT_CURR_BLOCK] = newBlock;
			desc_table[0][newBlock] = '1'; // Update bitmap
			if (DEBUG) {
				cout << "Bitmap updated at position: " << newBlock << endl;
			}
			bool found = false;
			for (int i=0; i < 3 && !found; ++i) {
				if (get_desc_block_value(oft[index][OFT_FILE_DESC_INDEX], i) == 0) {
					found = true;
					int desc_val = oft[index][OFT_FILE_DESC_INDEX];
					update_desc_block(desc_val, i, newBlock);
				}
			}
		}

		for (int i=0; i < count; ++i) {
			fputc(value, index);
		}
	}


	/* Setting new read/write position function:
	 * Parameter(s):
	 *    index: File index which indicates the file to be read.
	 *    pos: New position in the file. If pos is bigger than file size, set pos to file size.
	 * Return:
	 *    0 for successful write
	 *    -1 value for error case "File hasn't been open"
	 */
	int lseek(int index, int pos)
	{
		if (oft[index][OFT_OPEN_FLAG_INDEX] == 0)
			return FLAG_ERROR_NOTFOUND;

		if (pos > oft[index][OFT_FILE_SIZE]) {
			pos = oft[index][OFT_FILE_SIZE];
		}

		oft[index][OFT_CURR_POS_INDEX] = pos;
		return pos;
	}


	/* Close file function:
	 * Parameter(s):
	 *    index: The index of open file table
	 * Return:
	 *    none
	 */
	int close(int index)
	{
		if (index == 0)
			return FLAG_ERROR_NOTFOUND;

		if (oft[index][OFT_OPEN_FLAG_INDEX] == 0)
			return FLAG_ERROR_NOTFOUND;

		sys_io->write_block(oft[index][OFT_CURR_BLOCK], oft[index]);
		sys_io->saveDisk();
		clear_oft_buffer(index);

		oft[index][OFT_CURR_POS_INDEX] = 0;
		oft[index][OFT_OPEN_FLAG_INDEX] = 0;
		oft[index][OFT_FILE_DESC_INDEX] = 0;
		oft[index][OFT_FILE_DESC_INDEX] = FLAG_EMPTY;

		return FLAG_SUCCESS;
	}


	/* Delete file function:
	 *    Delete a file
	 * Parameter(s):
	 *    symbolic_file_name: a file name to be deleted.
	 * Return:
	 *    Return 0 with success
	 *    Return -1 with error (ie. No such file).
	 */
	int deleteFile(string fileName)
	{
		bool found = false;
		int file_pos;
		int directory_block = FLAG_ERROR_NOTFOUND;
		for (int i=0; i < 3; ++i) { // for each directory block
			int check_pos = search_dir(i, fileName);
			if (check_pos != FLAG_ERROR_NOTFOUND) {
				found = true;
				directory_block = get_desc_block_value(0, i);
				file_pos = check_pos;
			}
		}

		if (found) {
			if (DEBUG)
				cout << "File found now deleting at:" << file_pos << endl;
			sys_io->read_block(directory_block, oft[0]);

			// clear descriptor
			char desc_num[4];
			int file_inc = file_pos+4;
			for (int i=0; i < 4; ++i) {
				desc_num[i] = oft[0][file_inc++];
			}
			int numberfound = charArrayToNumber<int>(desc_num);

			// update bitmap
			for (int i=0; i < 3; ++i) {
				int bitmapIndex = get_desc_block_value(numberfound, i);\
				if (bitmapIndex > K) {
					desc_table[0][bitmapIndex] = FLAG_EMPTY;
				}
			}

			clear_descriptor(numberfound);

			// delete in oft
			oft[0][OFT_CURR_BLOCK] = directory_block;
			oft[0][OFT_CURR_POS_INDEX] = file_pos;
			for (int i=0; i < 8; ++i) {
				fputc(FLAG_EMPTY, 0);
			}

			// write to disk
			sys_io->write_block(oft[0][OFT_CURR_BLOCK], oft[0]);
			save();
			if (DEBUG)
				cout << sys_io->toString() << endl;
			return FLAG_SUCCESS;
		}
		return FLAG_ERROR_NOTFOUND;
	}


	/* Directory listing function:
	 *    List the name and size of files in the directory. (We have only one directory in this project.)
	 *    Example of format:
	 *       abc 66 bytes, xyz 22 bytes
	 * Parameter(s):
	 *    None
	 * Return:
	 *    None
	 */
	void directory()
	{
		for (int i=0; i < 4; ++i) { // For each directory block
			int curr_block = get_desc_block_value(0, i);
			if (curr_block != 0) {
				char* b = new char[64];
				sys_io->read_block(curr_block, b);
				char name[4];
				char desc_num[4];
				for (int j=0; j < BLOCK_SIZE; j += 8) {
					for (int k=0; k < 4; ++k) {
						if (isascii(b[j+k]))
							name[k] = b[j+k];
						else
							name[k] = ' ';
						if (isascii(b[j+4+k]))
							desc_num[k] = b[j+4+k];
						else
							desc_num[k] = ' ';
					}
					int desc_size = get_desc_size(charArrayToNumber<int>(desc_num));
					if (name[0] != '\0') {
						cout << name << " " << desc_size << endl;
					}
				}
			}
		}
	}

	/*------------------------------------------------------------------
	  Disk management functions.
	  These functions are not really a part of file system.
	  They are provided for convenience in this emulated file system.
	  ------------------------------------------------------------------
	 Restores the saved disk image in a file to the array.
	 */
	FileSystem53* restore(string diskName)
	{
		FileSystem53* f = new FileSystem53(64,64,diskName);

		if (f->sys_io) {
			f->sys_io->restoreDisk(diskName);

			for (int i=0; i < K; ++i) {
				f->sys_io->read_block(i, f->desc_table[i]);
			}
		}

		return f;
		// TODO: update OFT with directory
	}

	// Saves the array to a file as a disk image.
	void save()
	{
		for (int i=1; i < OFT_ROWS; ++i) {
			close(i);
		}

		for (int i=0; i < K; ++i) {
			sys_io->write_block(i, desc_table[i]);
		}

		sys_io->saveDisk();
	}

	// Disk dump, from block 'start' to 'start+size-1'.
	void diskdump(int start, int size)
	{
		for (int i=start; i < size; ++i) {
			sys_io->write_block(i, desc_table[i]);
		}
		sys_io->saveDisk();
	}

	template <typename T>
	void numberToCharArray(const T& Number, char* cstring)
	{
		ostringstream ss;
		ss << Number;
		strcpy(cstring, ss.str().c_str());
	}

	void numberToCharArray(int& number, char* cstring, int size)
	{
		for (int i=0; i < size; ++i) {
			cstring[i] = '0';
		}
		while(number > 0) {
			cstring[--size] = (char)(((int)'0')+(number % 10));
			number /= 10;
		}
	}

	template <typename T>
	T charArrayToNumber(const string& Text)
	{
		istringstream ss(Text);
	    T result;
	    return ss >> result ? result : 0;
	}

	string toString()
	{
		stringstream ss;
		for (int i=0; i < K; ++i) {
			for (int j=0; j < MAX_BLOCK_NO; ++j) {
				ss << desc_table[i][j];
			}
			ss << '\n';
		}
		return ss.str();
	}

	// This is aka cache. It's contents should be
	// maintained to be same as first K blocks in disk.
	// Descriptor table format:// maintained to be same as first K blocks in disk.
	// +-------------------------------------+
	// | bitmap | dsc_0 | dsc_1 | .. | dsc_N |
	// +-------------------------------------+
	//   bitmap: Each bit represent a block in a disk. MAX_BLOCK_NO/8 bytes
	//   dsc_0 : Root directory descriptor
	//   dsc_i : i'th descriptor. Each descriptor is FILE_SIZE_FIELD+ARRAY_SIZE bytes long.
	char** desc_table;  // Descriptor Table (in memory).
	char** oft;

	static const int MAX_BLOCK_NO = 64;       // Maximum number of blocks which can be supported by this file system.
	static const int BLOCK_SIZE = MAX_BLOCK_NO;
	static const int K = 7;  // Number of blocks for descriptor table

	static const int OFT_ROWS = 4;
	static const int OFT_COLS = BLOCK_SIZE + 5;
	static const int OFT_CURR_POS_INDEX = BLOCK_SIZE;
	static const int OFT_FILE_DESC_INDEX = BLOCK_SIZE + 1;
	static const int OFT_CURR_BLOCK = BLOCK_SIZE + 2;
	static const int OFT_FILE_SIZE = BLOCK_SIZE + 3;
	static const int OFT_OPEN_FLAG_INDEX = BLOCK_SIZE + 4;

	static const int FLAG_EMPTY = -1;
	static const int FLAG_ERROR_FULL = -100;
	static const int FLAG_ERROR_NOTFOUND = -404;
	static const int FLAG_ERROR_FILEEXISTS = -503;
	static const int FLAG_ERROR_EOF= -101;       // End-of-File
	static const int FLAG_SUCCESS = 1;

	// Filesystem format parameters:
	static const int FILE_SIZE_FIELD = 1;     // Size of file size field in bytes. Maximum file size allowed in this file system is 192.
	static const int ARRAY_SIZE = 3;          // The length of array of disk block numbers that hold the file contents.
	static const int DESCR_SIZE = FILE_SIZE_FIELD+ARRAY_SIZE;
	static const int MAX_FILE_NO = 24;        // Maximum number of files which can be stored by this file system.
	static const int MAX_BLOCK_NO_DIV8 = MAX_BLOCK_NO/8;
	static const int MAX_FILE_NAME_LEN = 32;  // Maximum size of file name in byte.
	static const int MAX_OPEN_FILE = 3;       // Maximum number of files to open at the same time.
	static const int FILEIO_BUFFER_SIZE = 64; // Size of file io bufer


    private:
	FileIO53* sys_io;

};
