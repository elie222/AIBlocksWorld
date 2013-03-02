package blocksWorld.Facts;

import blocksWorld.Box;

public class BWOnTableFact extends BWFact {

	private Box on;
	
	public BWOnTableFact(Box on){
		this.on = on;
	}
	
	@Override
	public boolean equals(Object f) {
		if(f instanceof BWOnTableFact)
			return on.equals(((BWOnTableFact) f).on);
		return false;
	}

	@Override
	public Box[] getBoxes() {
		Box[] b = new Box[1];
		b[0] = on;
		return b;
	}

	@Override
	public String toString() {
		return on.toString() + " ON TABLE";
	}

	@Override
	public BWFact dup() {
		return new BWOnTableFact(on.dup());
	}
}
