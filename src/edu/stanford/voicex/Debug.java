package edu.stanford.voicex;

public class Debug {
	public static final int TERSE = 1;
	public static final int NORMAL = 2;
	public static final int VERBOSE = 3;
	
	static int debugLevel = 1;
	
	
	public static int getDebugLevel() {
		return debugLevel;
	}


	public static void setDebugLevel(int logLevel) {
		debugLevel = logLevel;
	}


	public static void print(String msg, int loglevel){
		if(loglevel < debugLevel){
			System.out.println(msg);
		}
	}

}
