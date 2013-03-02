package blocksWorld;

import java.util.ArrayList;
import java.util.Collection;

import blocksWorld.Actions.BWAction;
import blocksWorld.Actions.BWPutOnTableAction;
import blocksWorld.Facts.BWFact;

import aStar.Node;

public class BWState implements Node<BWState>{

	private Collection<BWFact> facts;
	private boolean ArmEmpty;
	private Box holdByArm;
	
	public BWState(Collection<BWFact> facts, boolean ArmEmpty, Box holdByArm){
		this.ArmEmpty = ArmEmpty;
		this.facts = new ArrayList<BWFact>();
		this.facts.addAll(facts);
		this.holdByArm = holdByArm;
	}
	
	@Override
	public boolean equals(Object n) {
		if(n instanceof BWState){
			BWState k = (BWState) n;
			boolean a = false;
			for(BWFact f : k.facts){
				for(BWFact f1 : facts)
					if(f1.equals(f)){
						a = true;
						break;
					}
				if(!a)
					return false;
				a = false;
			}
			return  k.isArmEmpty() == ArmEmpty && ((k.getHoldByArm() == null && holdByArm == null) || k.getHoldByArm().equals(holdByArm));
		}
		return false;
	}

	@Override
	public Collection<BWState> getChildren() {
		Collection<BWState> children = new ArrayList<BWState>();
		Collection<BWAction> Actions = new ArrayList<BWAction>();
		for(BWFact fact : facts){
			BWAction ac = fact.getPosibleAction(ArmEmpty);
			if(ac != null)
				Actions.add(ac);
		}
		if(!ArmEmpty)
			Actions.add(new BWPutOnTableAction(null));
		for(BWAction ac : Actions)
			children.add(ac.perform(this));
		return children;
	}

	@Override
	public double getDistFromParent() {
		return 1;
	}
	
	public Collection<BWFact> getFacts(){
		return facts;
	}
	
	public boolean isArmEmpty(){
		return ArmEmpty;
	}

	public void setHoldByArm(Box holdByArm) {
		if(holdByArm == null)
			ArmEmpty = true;
		else ArmEmpty = false;
		this.holdByArm = holdByArm;
	}

	public Box getHoldByArm() {
		return holdByArm;
	}

	public String toString(){
		String s = "";
		s+= "ARMEMPTY = " + ArmEmpty + "\n\n";
		s+= "HOLDBYARM = " + holdByArm + "\n\n";
		s+= "FACTS:\n";
		for(BWFact f : facts)
			s+= f.toString() + "\n";
		return s;
	}
	
	public BWState dup(){
		Collection<BWFact> temp = new ArrayList<BWFact>();
		for(BWFact s : facts){
			temp.add(s.dup());
		}
		Box b = null;
		if(holdByArm != null)
			b = holdByArm.dup();
		return new BWState(temp,ArmEmpty,b);
	}
	
}
