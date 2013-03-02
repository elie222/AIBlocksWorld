package blocksWorld.Facts;

import blocksWorld.Box;
import blocksWorld.Actions.BWAction;

public abstract class BWFact {

	public abstract boolean equals(Object f);
	public BWAction getPosibleAction(boolean ArmEmpty){
		return null;
	}
	public abstract Box[] getBoxes();
	public abstract String toString();
	public abstract BWFact dup();
	
}
