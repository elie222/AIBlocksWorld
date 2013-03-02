package blocksWorld;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Random;
import java.util.Set;

import blocksWorld.Facts.BWFact;
import blocksWorld.Facts.BWFreeFact;
import blocksWorld.Facts.BWOnFact;
import blocksWorld.Facts.BWOnTableFact;

public class BWProbCreator {
	
	private String information;
	private BWState init;
	private BWState fin;
	private int BoxNum;
	
	private Collection<BWState> states = new ArrayList<BWState>();//for extracting all probs
	
	public BWProbCreator(int BoxNum){
		this.BoxNum = BoxNum;
	}
	
	public BWProbCreator(){
		
	}
	
	public void setInformation(String inf){
		information = inf;
	}
	
	public BWProbCreator(String loc) throws Exception{
	    StringBuilder contents = new StringBuilder();
	    
		BufferedReader input =  new BufferedReader(new FileReader(loc));
	    String line = null;
	    while (( line = input.readLine()) != null){
	    	contents.append(line);
	    	//contents.append(System.getProperty("line.separator"));
	    }
	    information = contents.toString();
	}
	
	public BWState createState(String[] s , Collection<Box> listOn, Collection<Box> listUnder){
		Collection<BWFact> facts = new ArrayList<BWFact>();
		Boolean armFree = true;
		Box holdByArm = null;
		
		if(!s[0].equals("INIT") && !s[0].equals("FIN")){
			System.out.println("File corupted line 37");
			System.exit(1);
		}
		
		for(int i = 1 ; i < s.length ; i++){
			if(s[i].matches(". ON .")){
				Box a = new Box(s[i].substring(0, 1));
				Box b = new Box(s[i].substring(5, 6));
				facts.add(new BWOnFact(a,b));
				listOn.remove(a);
				listUnder.remove(b);
			}else if(s[i].matches(". ON TABLE")){
				Box a = new Box(s[i].substring(0, 1));
				facts.add(new BWOnTableFact(a));
				listOn.remove(a);
			}else if(s[i].equals("ARMEMPTY")){
				armFree = true;
			}else if(s[i].equals(". HOLDBYARM")){
				armFree = false;
				holdByArm = new Box(s[i].substring(0, 1));
				listOn.remove(holdByArm);
				listUnder.remove(holdByArm);
			}	
		}
		
		if(!listOn.isEmpty()){
			//System.out.println(listOn);
			System.out.println("File corupted line 63");
			System.exit(1);
		}
		
		for(Box b : listUnder){
			facts.add(new BWFreeFact(b));
		}
		
		return new BWState(facts,armFree,holdByArm);
	}
	
	public void createProb(){
		String[] parts = information.split(";");
		String[] box = parts[0].split(",");
		
		Collection<Box> listOnInit = new ArrayList<Box>();
		Collection<Box> listUnderInit = new ArrayList<Box>();
		Collection<Box> listOnFin = new ArrayList<Box>();
		Collection<Box> listUnderFin = new ArrayList<Box>();
		
		for(String s : box){
			listOnInit.add(new Box(s.split(":")[1]));
			listUnderInit.add(new Box(s.split(":")[1]));
			listOnFin.add(new Box(s.split(":")[1]));
			listUnderFin.add(new Box(s.split(":")[1]));
		}
		
		init = createState(parts[1].split(","),listOnInit,listUnderInit);
		fin = createState(parts[2].split(","),listOnFin,listUnderFin);
		
	}
	
	public void generateRandomProb(){
		char[] c = {'A'};
		ArrayList<Box> b = new ArrayList<Box>();
		for(int  i  = 0 ; i < BoxNum ; i++){
			b.add(new Box(new String(c,0,1)));
			c[0]++;
		}
		init = new BWState(getRandFacts(new ArrayList<BWFact>(),new ArrayList<Box>(b),new ArrayList<Box>()),true,null);
		fin = new BWState(getRandFacts(new ArrayList<BWFact>(),new ArrayList<Box>(b),new ArrayList<Box>()),true,null);
	}
	
	public Collection<BWFact> getRandFacts(ArrayList<BWFact> Facts,ArrayList<Box> b,ArrayList<Box> free){
		if(b.isEmpty()){
			return Facts;
		}
		Random r = new Random();
		int temp = r.nextInt(free.size()+1);
		int temp1 = r.nextInt(b.size());
		Box box = b.get(temp1);
		if(temp == 0){
			Facts.add(new BWOnTableFact(box));
			Facts.add(new BWFreeFact(box));
			free.add(box);
			b.remove(box);
			return getRandFacts(Facts,b,free);
		}
		else{
			Facts.add(new BWOnFact(box,free.get(temp-1)));
			Facts.remove(new BWFreeFact(free.get(temp-1)));
			Facts.add(new BWFreeFact(box));
			free.remove(free.get(temp-1));
			free.add(box);
			b.remove(box);
			return getRandFacts(Facts,b,free);
		}
	}
	
	public void exportToFile(String file) throws Exception{
		Set<Box> s = new HashSet<Box>();
		for(BWFact f : init.getFacts()){
			if(f instanceof BWOnFact){
				s.add(f.getBoxes()[0]);
				s.add(f.getBoxes()[1]);
			}
			else s.add(f.getBoxes()[0]);
		}
		FileWriter fstream = new FileWriter(file);
		BufferedWriter out = new BufferedWriter(fstream);
		Box[] c = new Box[1];
		Box[] b = s.toArray(c);
		for(int i = 0 ; i < b.length ; i++)
			if(i == b.length-1)
				out.write("Box:"+b[i]+"\n");
			else out.write("Box:"+b[i]+",\n");
		out.write(";\n");
		out.write("INIT,\n");
		BWFact[] fff = new BWFact[1];
		BWFact[] f = init.getFacts().toArray(fff);
		for(int i = 0 ; i < f.length ; i++)
			if(!(f[i] instanceof BWFreeFact))
				out.write(f[i].toString()+",\n");
		out.write("ARMEMPTY\n");
		out.write(";\n");
		out.write("FIN,\n");
		BWFact[] f1 = fin.getFacts().toArray(fff);
		for(int i = 0 ; i < f1.length ; i++)
			if(!(f1[i] instanceof BWFreeFact))
				out.write(f1[i].toString()+",\n");
		out.write("ARMEMPTY");
		out.close();
		fstream.close();
	}
	
	public BWState getInitState(){
		return init;
	}
	
	public BWState getFinState(){
		return fin;
	}
	
	public Collection<BWProb> getAllProbs(){
		Collection<BWProb> y = new LinkedList<BWProb>();
		char[] c = {'A'};
		ArrayList<Box> b = new ArrayList<Box>();
		for(int  i  = 0 ; i < BoxNum ; i++){
			b.add(new Box(new String(c,0,1)));
			c[0]++;
		}
		getAllStates(new ArrayList<Box>(),new ArrayList<Box>(),b,new ArrayList<BWFact>());
		System.out.println(states.size());
		//long i = 0;
		for(BWState s : states)
			for(BWState r : states){
				y.add(new BWProb(s,r));
				//System.out.println(i++);
			}
		return y;				
	}
	
	public void getAllStates(ArrayList<Box> DontMove,ArrayList<Box> FreeBox,ArrayList<Box> list,ArrayList<BWFact> Facts){
		if(DontMove.size() == list.size()){
			states.add(new BWState(new ArrayList<BWFact>(Facts),true,null));
			return;
		}
		for(Box b : list){
			if(DontMove.contains(b))
				continue;
			Facts.add(new BWOnTableFact(b));
			Facts.add(new BWFreeFact(b));
			FreeBox.add(b);
			DontMove.add(b);
			getAllStates(DontMove,FreeBox,list,Facts);
			Facts.remove(new BWOnTableFact(b));
			for(Box f : list){
				if(!FreeBox.contains(f) || f.equals(b))
					continue;
				Facts.add(new BWOnFact(b,f));
				Facts.remove(new BWFreeFact(f));
				getAllStates(DontMove,FreeBox,list,Facts);
				Facts.remove(new BWOnFact(b,f));
				Facts.add(new BWFreeFact(f));
			}
			Facts.remove(new BWFreeFact(b));
			FreeBox.remove(b);
			DontMove.remove(b);
		}
	}
}
