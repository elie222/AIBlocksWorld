package blocksWorld.Actions;

import blocksWorld.BWState;
import blocksWorld.Box;
import blocksWorld.Facts.BWFact;
import blocksWorld.Facts.BWFreeFact;
import blocksWorld.Facts.BWOnTableFact;

public class BWPutOnTableAction extends BWAction {
	
	public BWPutOnTableAction(Box b) {
		super(b);
	}

	@Override
	public BWFact getPreCOndition() {
		return null;
	}

	@Override
	public BWState perform(BWState t) {
		BWState s = new BWState(t.getFacts(), t.isArmEmpty(), t.getHoldByArm());
		s.getFacts().add(new BWOnTableFact(s.getHoldByArm()));
		s.getFacts().add(new BWFreeFact(s.getHoldByArm()));
		s.setHoldByArm(null);
		return s;
	}

}
