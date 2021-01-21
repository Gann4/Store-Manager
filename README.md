# Store-Manager
A tool for store management, register incomes, outcomes, calculate prices and analyze your progress.<br>
'LDP Store Manager' is a software i'm creating for anyone who has a store and requires management, to keep track sales, incomes, outcomes, analyze data and calculate prices, for free.<br>

I don't recommend using it yet, since it is in a very early stage. Currently i'm looking for contributions, suggestions and discussions to improve this piece of software.<br>
<br>
## **Developer notes**
Before executing a file, make sure you're using the virtual enviroment provided.<br>
* Open your console and run `venv\Scripts\activate.bat`<br>
* Execute `LDP.py` with the python enviroment.<br>
<br>

**Example** _(cmd.exe)_:<br>
* `..\StoreManager > venv\Scripts\activate.bat`<br>
* `(venv) ..\StoreManager > python LDP.py`<br>

### **Execution policy error for PowerShell/VSCode**<br>
In case you get any error on a powershell console, you have to set the execution policy to `RemoteSigned`. <br>
Open powershell with admin permission and execute the following command: `Set-ExecutionPolicy RemoteSigned`.<br>

**Example** _(powershell.exe)_<br>
* `PS C:\Etc > Set-ExecutionPolicy RemoteSigned`


I wrote this section 'cause i might forgot that i need to run this on a virtual enviroment.<br>