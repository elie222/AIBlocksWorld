package blocksWorld.Actions;

import java.util.ArrayList;
import java.util.Collection;

import blocksWorld.BWState;
import blocksWorld.Box;
import blocksWorld.Facts.BWFact;

public abstract class BWAction {

	protected Box ActionOn;
	
	public BWAction(Box b){
		ActionOn = b;
	}
	
	public abstract BWFact getPreCOndition();

	public void setActionOn(Box actionOn) {
		ActionOn = actionOn;
	}

	public Box getActionOn() {
		return ActionOn;
	}
	
	public abstract BWState perform(BWState t);
	
	public static Collection<BWFact> getRelatedFacts(BWState s , Box box){
		Collection<BWFact> f = s.getFacts();
		Collection<BWFact> res = new ArrayList<BWFact>();
		for(BWFact t : f)
			for(Box b : t.getBoxes())
				if(b.equals(box)){
					res.add(t);
					break;
				}
		return res;
	}
	
}
