package blocksWorld.Facts;

import blocksWorld.Box;
import blocksWorld.Actions.BWAction;
import blocksWorld.Actions.BWPickUpAction;
import blocksWorld.Actions.BWPutOnAction;

public class BWFreeFact extends BWFact {

	Box free;
	
	public BWFreeFact(Box free){
		this.free = free;
	}
	
	@Override
	public boolean equals(Object f) {
		if(f instanceof BWFreeFact)
			return free.equals(((BWFreeFact) f).free);
		return false;
	}

	@Override
	public BWAction getPosibleAction(boolean ArmEmpty) {
		if(ArmEmpty)
			return new BWPickUpAction(free);
		else
			return new BWPutOnAction(free);
	}

	@Override
	public Box[] getBoxes() {
		Box[] b = new Box[1];
		b[0] = free;
		return b;
	}

	@Override
	public String toString() {
		return free.toString() + " FREE";
	}

	@Override
	public BWFact dup() {
		return new BWFreeFact(free.dup());
	}

}
