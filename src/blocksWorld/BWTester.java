package blocksWorld;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.Collection;
import java.util.Date;
import java.util.List;

import gridiAlgoForBW.RunGridi;
import blocksWorld.Huristic.*;
import blocksWorld.gui.NewJFrame;
import HillClimbing.HillClimbingHur;
import HillClimbing.runHillClimbing;
import aStar.RunAstar;

public class BWTester {
	
	public static void main(String[] args) throws Exception{
		/*BWProbCreator p = new BWProbCreator("src\\blocksWorld\\probs\\6blocks.prob");
		p.createProb();
		RunAstar<BWState> a = new RunAstar<BWState>(p.getFinState());
		RunAstar<BWState>.Results r = a.Search(p.getInitState(), new BWLearningHur());
		//RunAstar<BWState>.Results r = a.Search(p.getInitState(), new BWFactDistHur());
		System.out.println(r.nodesExpended);
		System.out.println(GetResults.getResults(r.path));
		System.out.println(r.path.size());*/
		
		java.awt.EventQueue.invokeLater(new Runnable() {
			public void run() {
				new NewJFrame().setVisible(true);
			}
		});
		
		/*BWProbCreator p = new BWProbCreator("src\\blocksWorld\\probs\\10blocks.prob");
		p.createProb();
		RunGridi g = new RunGridi(p.getFinState());
		Collection<BWState> r = g.run(p.getInitState());
		System.out.println(GetResults.getResults(r));
		System.out.println(r.size());*/

		/*BWProbCreator p = new BWProbCreator(20);
		p.generateRandomProb();
		p.exportToFile("src\\blocksWorld\\probs\\temp.prob");*/
		
		/*for(int i = 4 ; i < 20 ; i++){
			BWProbCreator p = new BWProbCreator(i);
			p.generateRandomProb();
			p.exportToFile("src\\blocksWorld\\probs\\"+i+"blocks.prob");
		}*/
		/*Date s = new Date();
		Date s1 = new Date();
		long start,end,TimeMiss = 0,TimeDist,TimeRed;
		FileWriter fstream = new FileWriter("src\\blocksWorld\\statics\\static4.csv");
		BufferedWriter out = new BufferedWriter(fstream);
		
		out.write("num,mis,dist,red\n");
		
		for(int i = 4 ; i < 12 ; i++){
			System.out.println("solving problem with " + i + " blocks");
			BWProbCreator p = new BWProbCreator("src\\blocksWorld\\probs\\"+i+"blocks.prob");
			p.createProb();
			RunAstar<BWState>.Results r1 = null;
			if(i <= 8){
			RunAstar<BWState> a = new RunAstar<BWState>(p.getFinState());
			s = new Date();
			start = s.getTime();
			r1 = a.Search(p.getInitState(), new BWFactMissingHur());
			s1 = new Date();
			end = s1.getTime();
			TimeMiss = end - start;
			}
			RunAstar<BWState> a1 = new RunAstar<BWState>(p.getFinState());
			s = new Date();
			start = s.getTime();
			RunAstar<BWState>.Results r2 = a1.Search(p.getInitState(), new BWFactDistHur());
			s1 = new Date();
			end = s1.getTime();
			TimeDist = end - start;
			
			RunAstar<BWState> a2 = new RunAstar<BWState>(p.getFinState());
			s = new Date();
			start = s.getTime();
			RunAstar<BWState>.Results r3 = a2.Search(p.getInitState(), new BWLearningHur());
			s1 = new Date();
			end = s1.getTime();
			TimeRed = end - start;
			if(r1 == null)
				out.write(i+","+0+","+TimeDist+","+ TimeRed +"\n");
			else out.write(i+","+TimeMiss+","+TimeDist+","+ TimeRed +"\n");
		}
		
		out.close();
		fstream.close();*/
		
		/*BWProbCreator p = new BWProbCreator(5);
		p.getAllProbs();*/
		
		/*int min = Integer.MAX_VALUE;
		for(int i = 0 ; i < 100 ; i++){
			BWProbCreator p = new BWProbCreator("src\\blocksWorld\\probs\\11blocks.prob");
			p.createProb();
			Collection<BWState> r = (new runHillClimbing<BWState>(p.getFinState())).Search(p.getInitState(),new BWFactDistHur());
			if(r.size() < min)
				min = r.size();
			System.out.println(r.size());
		}
		System.out.println("-------------------------------");
		System.out.println(min);*/
		
		/*BWProbCreator p = new BWProbCreator("src\\blocksWorld\\probs\\8blocks.prob");
		p.createProb();
		Collection<BWState> r = (new runHillClimbing<BWState>(p.getFinState())).Search(p.getInitState(),new HillClimbingHur());
		System.out.println(GetResults.getResults(r));
		System.out.println(r.size());*/
		
	}
}
