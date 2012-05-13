package edu.stanford.voicex;

public class Debug {
	public static final int TERSE = 1;
	public static final int NORMAL = 2;
	public static final int VERBOSE = 3;
	
	public static void print(String msg, int loglevel){
		System.out.println(msg);
	}

}
