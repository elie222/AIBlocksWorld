package blocksWorld.Actions;

import java.util.Collection;

import blocksWorld.BWState;
import blocksWorld.Box;
import blocksWorld.Facts.BWFact;
import blocksWorld.Facts.BWFreeFact;

public class BWPickUpAction extends BWAction{

	public BWPickUpAction(Box b){
		super(b);
	}
	
	@Override
	public BWFact getPreCOndition() {
		return new BWFreeFact(getActionOn());
	}

	@Override
	public BWState perform(BWState t) {
		boolean isAlowed = false;
		BWState s = new BWState(t.getFacts(), t.isArmEmpty(), t.getHoldByArm());
		Collection<BWFact> relatedFacts = getRelatedFacts(s,ActionOn);
		for(BWFact fact : relatedFacts)
			if(fact.equals(getPreCOndition()))
				isAlowed = true;
		if(!isAlowed){
			System.out.println("action is not alowed it shouldnt be happend");
			System.exit(1);
		}
		for(BWFact fact : relatedFacts)
			if(fact.getBoxes().length == 2){
				s.getFacts().add(new BWFreeFact(fact.getBoxes()[1]));
				s.setHoldByArm(fact.getBoxes()[0]);
			}else s.setHoldByArm(fact.getBoxes()[0]);
		s.getFacts().removeAll(relatedFacts);
		return s;
	}
}
