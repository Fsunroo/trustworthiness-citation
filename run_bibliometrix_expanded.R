args <- commandArgs(trailingOnly=TRUE)
base <- if(length(args)) normalizePath(args[[1]]) else getwd()
suppressPackageStartupMessages(library(bibliometrix))
M <- read.csv(file.path(base,'bibliometrix_expanded.csv'),na.strings='',check.names=FALSE,stringsAsFactors=FALSE)
M$CR<-as.character(M$CR);M$DI<-as.character(M$DI);M$DE<-as.character(M$DE);M$ID<-as.character(M$ID)
# A semicolon inside the 1950 Brier DOI is a valid DOI character, but is
# also the CR delimiter. Omit that DOI only from computational matching;
# canonical node labels still resolve it, and original DOI remains in input/evidence.
bad_doi <- unique(M$DI[!is.na(M$DI) & grepl(';',M$DI,fixed=TRUE)])
for (d in bad_doi) {
 M$CR <- gsub(paste0(', DOI ',toupper(d)),'',M$CR,fixed=TRUE)
 M$DI[M$DI==d & !is.na(M$DI)] <- NA_character_
}
expected<-read.csv(file.path(base,'expected_edges.csv'),stringsAsFactors=FALSE)
H<-histNetwork(M,sep=';',network=TRUE,verbose=TRUE)
raw<-as.matrix(H$NetMatrix)
HM<-H$M
mat<-matrix(0L,nrow(HM),nrow(HM),dimnames=list(HM$LABEL,HM$LABEL))
for(i in seq_len(nrow(HM))) {
 if(is.na(HM$LCR[i])||!nzchar(HM$LCR[i]))next
 target<-match(trimws(strsplit(HM$LCR[i],';',fixed=TRUE)[[1]]),trimws(HM$LABEL))
 stopifnot(!anyNA(target));mat[i,unique(target)]<-1L
}
# Reconcile the 5.5.0 empty-DOI trailing-space issue using native LCR only.
native_lcs<-setNames(H$histData$LCS,H$histData$Paper)
stopifnot(all(colSums(mat)==native_lcs[colnames(mat)]))
key<-setNames(HM$ARTICLE_ID,HM$LABEL);pos<-which(mat>0,arr.ind=TRUE)
edges<-data.frame(source=unname(key[rownames(mat)[pos[,1]]]),target=unname(key[colnames(mat)[pos[,2]]]))
cat('Recovered',nrow(edges),'Expected',nrow(expected),'\n');print(expected[!paste(expected$source,expected$target)%in%paste(edges$source,edges$target),]);stopifnot(!anyNA(edges),nrow(edges)==nrow(expected),setequal(paste(edges$source,edges$target),paste(expected$source,expected$target)))
cat('Raw matrix edges:',sum(raw),'; reconciled native LCR edges:',sum(mat),'\n')
H$NetMatrix<-mat
write.csv(edges,file.path(base,'bibliometrix_validated_edges.csv'),row.names=FALSE)
write.csv(H$histData,file.path(base,'bibliometrix_histData.csv'),row.names=FALSE)
saveRDS(H,file.path(base,'bibliometrix_expanded_histResults.rds'))
# Plot a readable subset: all 45 source papers plus the top 25 cited-reference nodes.
nodes<-jsonlite::fromJSON(file.path(base,'expanded_network.json'))$nodes
refs<-nodes[nodes$kind=='cited_reference',];top<-head(refs$id,25)
selected<-nodes$id[nodes$kind=='included'|nodes$id%in%top]
idx<-which(HM$ARTICLE_ID%in%selected)
small<-H;small$NetMatrix<-mat[idx,idx,drop=FALSE];small$histData<-H$histData[idx,,drop=FALSE]
set.seed(20261016)
plot<-histPlot(small,n=length(idx),size=3,labelsize=2.4,remove.isolates=TRUE,label='short',verbose=FALSE)
saveRDS(plot,file.path(base,'bibliometrix_expanded_focus_histPlot.rds'))
if(!is.null(plot$g))ggplot2::ggsave(file.path(base,'bibliometrix_native_focus.png'),plot$g,width=20,height=15,dpi=200)
writeLines(capture.output(sessionInfo()),file.path(base,'R_sessionInfo.txt'))
cat('VALIDATED:',nrow(HM),'total nodes;',nrow(edges),'direct edges; all',sum(nodes$kind=='included'),'source papers retained in full data.\n')
