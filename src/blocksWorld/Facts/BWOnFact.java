package blocksWorld.Facts;

import blocksWorld.Box;

public class BWOnFact extends BWFact{

	private Box up;
	private Box down;
	
	public BWOnFact(Box up, Box down){
		this.up = up;
		this.down = down;
	}
	
	@Override
	public boolean equals(Object f) {
		if(f instanceof BWOnFact)
			return up.equals(((BWOnFact) f).up) && down.equals(((BWOnFact) f).down);
		return false;
	}

	@Override
	public Box[] getBoxes() {
		Box[] b = new Box[2];
		b[0] = up;
		b[1] = down;
		return b;
	}

	@Override
	public String toString() {
		return up.toString() + " ON " + down.toString();
	}

	@Override
	public BWFact dup() {
		return new BWOnFact(up.dup(),down.dup());
	}
}
