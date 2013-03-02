package blocksWorld.Actions;
import java.util.Collection;

import blocksWorld.BWState;
import blocksWorld.Box;
import blocksWorld.Facts.BWFact;
import blocksWorld.Facts.BWFreeFact;
import blocksWorld.Facts.BWOnFact;

public class BWPutOnAction extends BWAction{

	public BWPutOnAction(Box b) {
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
		s.getFacts().remove(new BWFreeFact(ActionOn));
		s.getFacts().add(new BWOnFact(s.getHoldByArm(),ActionOn));
		s.getFacts().add(new BWFreeFact(s.getHoldByArm()));
		s.setHoldByArm(null);
		return s;
	}
	
}
