args <- commandArgs(trailingOnly = TRUE)
file<-args[1]
scale<-args[2]

if(scale=="alphahelix"){def<-"Alpha-helix (Deleage-Roux, 1987)"}
if(scale=="betasheet"){def<-"Beta-sheet (Chou-Fasman, 1978)"}
if(scale=="disorder"){def<-"Disorder (Dunker, 2008)"}
if(scale=="hydrophobicity"){def<-"Hydrophobicity (Eisenberg, 1984)"}

tab<-read.table(file)

png("outputs/profile.png")
plot(smooth.spline(t(tab[-1]),
	df=dim(tab[-1])[2]/2),
	type="l",lwd=4,col="tomato",
	xlab="protein sequence",
	ylab=def)
dev.off()
