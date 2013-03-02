package blocksWorld;

public class BWProb {
	private BWState init;
	private BWState fin;
	private int numberOfStaps;
	
	public BWProb(BWState init, BWState fin){
		this.init = init;
		this.fin = fin;
	}
	
	public BWProb(BWState init, BWState fin, int size) {
		this.init = init;
		this.fin = fin;
		this.numberOfStaps = size;
	}

	public void setInit(BWState init) {
		this.init = init;
	}
	public BWState getInit() {
		return init;
	}
	public void setFin(BWState fin) {
		this.fin = fin;
	}
	public BWState getFin() {
		return fin;
	}
	public void setNumberOfStaps(int numberOfStaps) {
		this.numberOfStaps = numberOfStaps;
	}
	public int getNumberOfStaps() {
		return numberOfStaps;
	}
	
	public boolean equals(Object o){
		if(o instanceof BWProb){
			BWProb t = (BWProb) o;
			return init.equals(t.getInit()) && init.equals(t.getInit());
		}
		return false;
	}
}
