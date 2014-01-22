import java.io.*; 
import java.net.*; 
import java.util.*; 

class TCPClient {
	static Socket clientSocket;
	static BufferedReader inFromServer;
	static DataOutputStream outToServer;

	public static void main(String argv[]) throws Exception  {
		System.out.println("Welcome :)");
		System.out.println(argv[0]);
		String ip = argv[0];
		int port = Integer.parseInt(argv[1]);
		connect(ip, port);
		send();
		listen();
	}

	public static void connect(String ip, int port) throws Exception {
		clientSocket = new Socket("127.0.0.1", 1337);
		inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
		outToServer = new DataOutputStream(clientSocket.getOutputStream());
	}

	public static void listen() throws Exception {
		String response;
		response = inFromServer.readLine();   
		System.out.println("FROM SERVER: " + response);
		clientSocket.close();
	}
	public static void send() throws Exception {
		BufferedReader inFromUser = new BufferedReader( new InputStreamReader(System.in));
		String sentence;
		sentence = inFromUser.readLine();
		outToServer.writeBytes(sentence + '\n');   
	}
};
