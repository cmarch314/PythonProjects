//============================================================================
// Name        : project01.cpp
// Author      : Gregory Jeckell
// Version     :
// Copyright   : 
// Description : Hello World in C++, Ansi-style
//============================================================================

#include "FileSystem53.cpp"
using namespace std;

void displayCommands();
void create(string name);
void destroy(string name);
void open(string name);
void close(int index);
void read(int index, int count);
void write(int index, char chartowrite, int count);
void seek(int index, int pos);
void directory();
void init(string disk);
void load(string disk);
void save();
void callFileSystem(string[6]);
char convertStringToChar(string str);

FileSystem53* fileSystem;

int main()
{
	const int MAX_ARGS = 6;
	string line;
	displayCommands();
	cout << "Please enter a command from this list!" << endl;

	while(true){

	cout << "$ ";
	getline(cin, line);

    istringstream iss(line);

    string argv[MAX_ARGS];

    //load command and args into array
    for (int i = 0; i < MAX_ARGS; i++)
    	iss >> argv[i];

    //call appropriate filesystem command with given arguments
    callFileSystem(argv);


}//end while

	return 0;
}//end main



void displayCommands(){

	cout << "cr <name> : Create a file" << endl;
	cout << "de <name> : Destroy a file" << endl;
	cout << "op <name> : Open a file" << endl;
	cout << "cl <index> : Close a file" << endl;
	cout << "rd <index> : Read a file" << endl;
	cout << "wr <index> <char> <count> : Write to an open file" << endl;
	cout << "sk <index> <pos> : Seek to new position" << endl;
	cout << "dr : Display file directory" << endl;
	cout << "in <disk_cont> : Initialize disk" << endl;
	cout << "ld <disk cont> : Restore disk" << endl;
	cout << "sv  : Save disk" << endl;
}

void create(string name) {
	if (!fileSystem) {
		cout << "File system does not exist yet" << endl;
		return;
	}

	int msg = fileSystem->create(name);
	if (msg == fileSystem->FLAG_ERROR_FULL)
		cout << "error: disk is full" << endl;
	else if (msg == fileSystem->FLAG_ERROR_FILEEXISTS)
		cout << "error: file already exists" << endl;
	else
		cout << "file " << name << " created" << endl;
}
void destroy(string name) {
	if (!fileSystem) {
		cout << "File system does not exist yet" << endl;
		return;
	}

	if (fileSystem->deleteFile(name) == fileSystem->FLAG_ERROR_NOTFOUND){
		cout << "error: file not found" << endl;
	}
	else
		cout << "file " << name << " destroyed" << endl;
}

void open(string name) {
	if (!fileSystem) {
		cout << "File system does not exist yet" << endl;
		return;
	}

	int msg = fileSystem->open(name);
	if (msg == fileSystem->FLAG_ERROR_NOTFOUND){
		cout << "error: file not found" << endl;
	}
	else if (msg == fileSystem->FLAG_ERROR_FULL){
		cout << "error: disk is full" << endl;
	}
	else
		cout << "file " << name << " opened, index=" << msg << endl; //return index
}

void close(int index) {
	if (!fileSystem) {
		cout << "File system does not exist yet" << endl;
		return;
	}

	if (index == 0)
		cout << "error: cannot close directory file" << endl;
	else
		if (index > fileSystem->MAX_OPEN_FILE ||
				fileSystem->close(index) == fileSystem->FLAG_ERROR_NOTFOUND){
			cout << "error: invalid OFT index" << endl;
		} else {
			cout << "file " << index << " closed" << endl;
		}
}

void read(int index, int count) {
	if (!fileSystem) {
		cout << "File system does not exist yet" << endl;
		return;
	}

	int readReturn = fileSystem->read(index, count);
	if (readReturn == fileSystem->FLAG_ERROR_NOTFOUND){
		cout << "error: file not found" << endl;
	}
	else
		cout << endl << " bytes read: " << readReturn << endl; //successful read
}

void write(int index, char chartowrite, int count) {
	if (!fileSystem) {
		cout << "File system does not exist yet" << endl;
		return;
	}

	int msg = fileSystem->write(index, chartowrite, count);
	if (msg == fileSystem->FLAG_ERROR_NOTFOUND){
		cout << "error: no open file found" << endl;
	}
	else
		if (msg == fileSystem->FLAG_ERROR_FULL){
			cout << "error: file is full" << endl;
		}
		else
			cout << count << " bytes written" << endl; //successful write
}

void seek(int index, int pos) {
	if (!fileSystem) {
		cout << "File system does not exist yet" << endl;
		return;
	}

	if (fileSystem->lseek(index, pos) == fileSystem->FLAG_ERROR_NOTFOUND){
		cout << "error: no open file found" << endl;
	}
	else
		cout << "current position is " << pos << endl;
}

void directory() {
	if (!fileSystem) {
		cout << "File system does not exist yet" << endl;
		return;
	}

	cout << "shell.directory" << endl;
	fileSystem->directory();
}

void init(string disk) {
	cout << "This system currently supports only a 64x64 disk" << endl;
	delete fileSystem;
	fileSystem = new FileSystem53(64, 64, disk);

	cout << "disk initialized" << endl;
}

void load(string disk) {
	if (fileSystem)
		delete fileSystem;
	fileSystem = fileSystem->restore(disk);
}

void save() { //parameter for save was unused!!
	fileSystem->save();
	cout << "disk saved" << endl;
}

void callFileSystem(string argv[6]){
	string command = argv[0];

	if (command == "cr"){
		string name = argv[1];
		create(name);
	}
	else
	if (command == "de"){
		string name = argv[1];
		destroy(name);
	}
	else
	if (command == "op"){
		//string name = argv[1];
		open(argv[1]);
	}
	else
	if (command == "cl"){
		int index = atoi(argv[1].c_str());
		close(index);
	}
	else
	if (command == "rd"){
		int index = atoi(argv[1].c_str());
		int count = atoi(argv[2].c_str());
		read(index, count);
	}
	else
	if (command == "wr"){
		int index = atoi(argv[1].c_str());
		int count = atoi(argv[3].c_str());
		write(index, convertStringToChar(argv[2]), count);
	}
	else
	if (command == "sk"){
		int index = atoi(argv[1].c_str());
		int pos = atoi(argv[2].c_str());
		seek(index, pos);
	}
	else
	if (command == "dr"){
		directory();
	}
	else
	if (command == "in"){
		init(argv[1]);
	}
	else
	if (command == "sv"){
		save();
	}
	else
	if (command == "ld") {
		load(argv[1]);
	}
	else{
		cout << "error: not a valid command" << endl;
		displayCommands();
	}

}

char convertStringToChar(string str){
   int lengthOfString=str.length();

   char characters[lengthOfString];

   str.copy( characters, lengthOfString );
   return  characters[0];
}

/*
    //test contents of array
    for (int i = 0; i < MAX_ARGS; i++)
     	cout << "argv[" << i << "] " << argv[i] << " "; cout << endl;
*/
